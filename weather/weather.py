# https://github.com/ktreewriter/mcp_helloworld

from typing import Any, Dict
import os
import httpx
import xmltodict
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("korea_weather")

# API 상수 정의
API_BASE = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
USER_AGENT = "korea-weather-app/1.0"

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

# 환경 변수에서 서비스 키 가져오기
SERVICE_KEY = os.environ.get("DATA_SERVICE_KEY", "")

# 강수형태 코드 매핑
PTY_CODE = {
    "0": "없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "4": "소나기",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}

# 풍향 16방위
WIND_DIRECTIONS = [
    "북(N)", "북북동(NNE)", "북동(NE)", "동북동(ENE)",
    "동(E)", "동남동(ESE)", "남동(SE)", "남남동(SSE)",
    "남(S)", "남남서(SSW)", "남서(SW)", "서남서(WSW)",
    "서(W)", "서북서(WNW)", "북서(NW)", "북북서(NNW)"
]

# 날씨 카테고리 코드 설명
CATEGORY_DESCRIPTIONS = {
    "T1H": "기온",
    "RN1": "1시간 강수량",
    "UUU": "동서바람성분",
    "VVV": "남북바람성분",
    "REH": "습도",
    "PTY": "강수형태",
    "VEC": "풍향",
    "WSD": "풍속"
}

# 날씨 카테고리 단위
CATEGORY_UNITS = {
    "T1H": "°C",
    "RN1": "mm",
    "UUU": "m/s",
    "VVV": "m/s",
    "REH": "%",
    "PTY": "",
    "VEC": "°",
    "WSD": "m/s"
}

def get_wind_direction(vec: float) -> str:
    """
    풍향값(degree)을 16방위로 변환한다.
    
    Args:
        vec: 풍향 각도 (0-360)
        
    Returns:
        16방위 문자열 (예: '북(N)', '북동(NE)')
    """
    # (풍향값 + 22.5 * 0.5) / 22.5 = 변환값(소수점 이하 버림)
    convert_val = int((vec + 22.5 * 0.5) / 22.5)
    if convert_val >= 16:
        convert_val = 0
    return WIND_DIRECTIONS[convert_val]

async def make_api_request(url: str, params: dict) -> Dict[str, Any] | None:
    """
    한국 기상청 API에 요청을 보내고 응답을 처리한다.
    
    Args:
        url: API 엔드포인트 URL
        params: 요청 파라미터 딕셔너리
        
    Returns:
        XML 응답을 파싱한 딕셔너리 또는 오류 정보
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/xml"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return xmltodict.parse(response.text)
        except Exception as e:
            return {"error": str(e)}

def get_current_date() -> str:
    """
    현재 날짜를 YYYYMMDD 형식의 문자열로 반환한다.
    
    Returns:
        YYYYMMDD 형식의 날짜 문자열
    """
    return datetime.now().strftime("%Y%m%d")

def get_current_time() -> str:
    """
    적절한 API 호출을 위한 base_time을 계산하여 반환한다.
    기상청 API는 매시간 정시에 생성되고 10분 이후에 호출 가능하므로,
    현재 시간이 정시로부터 10분 이내라면 이전 시간대 데이터를 사용한다.
    
    Returns:
        HHMM 형식의 기준 시각 문자열 (분은 항상 00)
    """
    now = datetime.now()
    # 현재 시간이 정시로부터 10분 이내라면 이전 시간대 데이터 사용
    if now.minute < 10:
        now = now - timedelta(hours=1)
    
    # 시간을 HHMM 형식으로 변환 (정시이므로 분은 00)
    return f"{now.hour:02d}00"

def format_weather_data(items: list) -> Dict[str, str]:
    """
    API 응답에서 받은 날씨 데이터를 사용자 친화적인 형태로 가공한다.
    
    Args:
        items: API 응답에서 추출한 날씨 항목 리스트
        
    Returns:
        카테고리별로 가공된 날씨 정보 딕셔너리
    """
    weather_data = {}
    
    for item in items:
        category = item['category']
        value = item['obsrValue']
        
        # 카테고리별 처리
        if category == "T1H":  # 기온
            weather_data['temperature'] = f"{value}{CATEGORY_UNITS[category]}"
            
        elif category == "RN1":  # 1시간 강수량
            weather_data['rainfall'] = f"{value}{CATEGORY_UNITS[category]}"
            
        elif category == "UUU":  # 동서바람성분
            # 양수: 동, 음수: 서
            direction = "동" if float(value) >= 0 else "서"
            weather_data['east_west_wind'] = f"{abs(float(value)):.1f}{CATEGORY_UNITS[category]} ({direction})"
            
        elif category == "VVV":  # 남북바람성분
            # 양수: 북, 음수: 남
            direction = "북" if float(value) >= 0 else "남"
            weather_data['north_south_wind'] = f"{abs(float(value)):.1f}{CATEGORY_UNITS[category]} ({direction})"
            
        elif category == "REH":  # 습도
            weather_data['humidity'] = f"{value}{CATEGORY_UNITS[category]}"
            
        elif category == "PTY":  # 강수형태
            precip_desc = PTY_CODE.get(value, "알 수 없음")
            weather_data['precipitation_type'] = f"{precip_desc} (코드: {value})"
            
        elif category == "VEC":  # 풍향
            wind_dir = get_wind_direction(float(value))
            weather_data['wind_direction'] = f"{value}{CATEGORY_UNITS[category]} ({wind_dir})"
            
        elif category == "WSD":  # 풍속
            weather_data['wind_speed'] = f"{value}{CATEGORY_UNITS[category]}"
    
    return weather_data

@mcp.tool()
async def get_current_weather(nx: str, ny: str) -> str:
    """
    특정 지점의 현재 날씨 정보를 가져온다.
    
    Args:
        nx: 예보지점 X 좌표 (기상청 좌표계 기준)
        ny: 예보지점 Y 좌표 (기상청 좌표계 기준)
        
    Returns:
        현재 날씨 정보를 포맷팅한 문자열
    """
    if not SERVICE_KEY:
        return "서비스 키가 설정되지 않았습니다. 환경 변수를 확인해주세요."
    
    url = f"{API_BASE}/getUltraSrtNcst"
    base_date = get_current_date()
    base_time = get_current_time()
    
    params = {
        'serviceKey': SERVICE_KEY,
        'pageNo': '1',
        'numOfRows': '30',  # 충분한 수의 항목을 가져오기 위해 증가
        'dataType': 'XML',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }
    
    data = await make_api_request(url, params)
    if not data or "response" not in data:
        return "날씨 정보를 가져올 수 없습니다."
    
    try:
        # 응답 결과 코드 확인
        result_code = data['response']['header']['resultCode']
        if result_code != '00':
            result_msg = data['response']['header']['resultMsg']
            return f"API 오류: {result_msg} (코드: {result_code})"
        
        items = data['response']['body']['items']['item']
        if not items:
            return "해당 지역의 날씨 정보가 없습니다."
        
        # 날씨 데이터 가공
        weather_data = format_weather_data(items)
        
        # 결과 포맷팅
        result = f"""# 현재 날씨 정보
        - 위치: 격자좌표 (X:{nx}, Y:{ny})
        - 기준 시간: {base_date} {base_time}

        ## 기상 상태
        - 기온: {weather_data.get('temperature', 'N/A')}
        - 습도: {weather_data.get('humidity', 'N/A')}
        - 강수형태: {weather_data.get('precipitation_type', 'N/A')}
        - 1시간 강수량: {weather_data.get('rainfall', 'N/A')}

        ## 바람 정보
        - 풍향: {weather_data.get('wind_direction', 'N/A')}
        - 풍속: {weather_data.get('wind_speed', 'N/A')}
        - 동서바람성분: {weather_data.get('east_west_wind', 'N/A')}
        - 남북바람성분: {weather_data.get('north_south_wind', 'N/A')}
        """
        return result
    except Exception as e:
        return f"날씨 정보 처리 중 오류가 발생했습니다: {str(e)}"

import asyncio
if __name__ == "__main__":
    # 서버 초기화 및 실행
    mcp.run(transport='stdio')
    
    # async def main():
    #     result = await get_current_weather("60", "127")  # 서울 중구 격자좌표
    #     print(result)
    # asyncio.run(main())