from pydantic import BaseModel

class MCPRequest(BaseModel):
    query: str

class MCPResponse(BaseModel):
    context: str
    final_answer: str