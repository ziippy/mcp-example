import streamlit as st
import requests

import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except:
        enc = tiktoken.get_encoding("cl100k_base")  # fallback
    return len(enc.encode(text))

st.set_page_config(page_title="MCP 검색 + GPT 응답", layout="centered")

st.title("🔎 MCP Server 기반 검색 + GPT 응답")

# 입력 폼
with st.form("mcp_form"):
    query = st.text_input("검색어", placeholder="예: LangGraph는 무엇인가요?")
    openai_key = st.text_input("OpenAI API Key", type="password")
    serper_key = st.text_input("Serper API Key", type="password")
    submit = st.form_submit_button("질문하기")

if submit:
    if not all([query, openai_key, serper_key]):
        st.warning("모든 필드를 입력해주세요.")
    else:
        with st.spinner("MCP Server에 요청 중..."):
            try:
                response = requests.post(
                    "http://localhost:8000/mcp",
                    headers={
                        "X-OpenAI-API-Key": openai_key,
                        "X-Serper-API-Key": serper_key
                    },
                    json={"query": query},
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()

                st.success("✅ 요청 성공!")

                st.subheader("📚 요약된 검색 결과")
                st.markdown(result["context"])

                # 응답 텍스트
                gpt_answer = result["final_answer"]

                st.subheader("💬 GPT 응답")
                st.markdown(gpt_answer)                

                # 토큰 수 계산
                token_count = count_tokens(gpt_answer, model="gpt-4o")

                st.subheader("📊 응답 토큰 수")
                st.markdown(f"총 **{token_count} tokens**")

                # 시각적 표시 (progress bar 기준: 4096 = GPT-4o context 예시)
                max_token = 8192  # gpt-4o 기준 총 context limit
                st.progress(min(token_count, max_token) / max_token)

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
