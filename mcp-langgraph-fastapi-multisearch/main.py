from fastapi import FastAPI
from models.schema import MCPRequest, MCPResponse
from graph import build_graph

app = FastAPI()
graph = build_graph()

@app.post("/mcp", response_model=MCPResponse)
def handle_mcp(req: MCPRequest):
    state = { "query": req.query }
    result = graph.invoke(state)
    return MCPResponse(context=result["context"], final_answer=result["answer"])

# 로컬 테스트용 실행 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)