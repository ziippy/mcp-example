from langgraph.graph import StateGraph, END
from tools.search_tool import search_google
from tools.chat_tool import chat_completion
from state import MCPState


# 1. 검색 노드
def search_node(state: MCPState) -> MCPState:
    context = search_google(state["query"])
    return { **state, "context": context }

# 2. Chat 노드
def chat_node(state: MCPState) -> MCPState:
    prompt = f"다음 검색 결과를 참고하여 질문 '{state['query']}'에 답해주세요:\n\n{state['context']}"
    answer = chat_completion(prompt)
    return { **state, "answer": answer }


# 3. LangGraph 구성
def build_graph():
    builder = StateGraph(MCPState)

    builder.add_node("search", search_node)
    builder.add_node("chat", chat_node)

    builder.set_entry_point("search")
    builder.add_edge("search", "chat")
    builder.add_edge("chat", END)

    return builder.compile()

# 4. 실행
if __name__ == "__main__":
    graph = build_graph()
    user_query = input("검색어를 입력하세요: ")
    result = graph.invoke({ "query": user_query })

    print("\n🔎 검색 결과 요약:\n", result["context"])
    print("\n💬 ChatGPT 답변:\n", result["answer"])