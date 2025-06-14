from fastapi import FastAPI
from models.schema import MCPRequest, MCPResponse
from tools.search_tool import search_google
from tools.chat_tool import chat_completion

app = FastAPI()

@app.post("/mcp", response_model=MCPResponse)
def process_mcp(request: MCPRequest):
    # Step 1: 검색
    context = search_google(request.query)

    # Step 2: GPT로 최종 응답 생성
    final_answer = chat_completion(f"다음 검색 결과를 참고해서 사용자 질문에 답변해줘:\n\n{context}")

    return MCPResponse(context=context, final_answer=final_answer)