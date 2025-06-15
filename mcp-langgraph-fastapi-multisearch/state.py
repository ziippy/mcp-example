from typing import TypedDict, Optional

class MCPState(TypedDict):
    query: str
    context: Optional[str]
    answer: Optional[str]