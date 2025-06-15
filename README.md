MCP Example

시나리오: "검색어 입력 → Serper 검색 → OpenAI Chat Completion → 응답 반환"

- mcp-server
  - Python + FastAPI 기반 MCP Server

- mcp-langgraph
  - LangGraph 기반 MCP Server // 단순 호출용

- mcp-langgraph-fastapi
  - [POST /mcp] → LangGraph Graph 실행 → 응답 반환


사용법
- API-KEY 가 고정된 경우
  - curl -X POST http://localhost:8000/mcp   -H "Content-Type: application/json"   -d '{"query": "대한민국의 21대 대통령 이름?"}'

- API-KEY 가 가변적인 경우
  - curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "X-OpenAI-API-Key: sk-xxx" \
  -H "X-Serper-API-Key: serper-yyy" \
  -d '{"query": "LangGraph란?"}'

- streamlit app 기반
  - streamlit run app.py