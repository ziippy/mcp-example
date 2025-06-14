MCP Example

시나리오: "검색어 입력 → Serper 검색 → OpenAI Chat Completion → 응답 반환"

- mcp-server
  - Python + FastAPI 기반 MCP Server

- mcp-langgraph
  - LangGraph 기반 MCP Server // 단순 호출용

- mcp-langgraph-fastapi
  - [POST /mcp] → LangGraph Graph 실행 → 응답 반환
