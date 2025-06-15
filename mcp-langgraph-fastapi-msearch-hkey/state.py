from typing import TypedDict, Optional

class MCPState(TypedDict):
    query: str
    openai_api_key: Optional[str]
    serper_api_key: Optional[str]
    context: Optional[str]
    answer: Optional[str]