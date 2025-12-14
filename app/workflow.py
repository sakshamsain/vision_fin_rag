# app/workflow.py

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from .retrieval import retrieve_pages  
from .graph_store import get_facts_for_question
from .llm import generate_answer  


class RAGState(TypedDict):
    question: str
    pages: List[str]
    facts: List[str]
    answer: str


def node_retrieve_pages(state: RAGState) -> RAGState:
    q = state["question"]
    pages = retrieve_pages(q)        # returns list[str] summaries or texts
    state["pages"] = pages
    return state


def node_query_graph(state: RAGState) -> RAGState:
    q = state["question"]
    facts = get_facts_for_question(q)   # returns list[str] like "Revenue 2023 = ..."
    state["facts"] = facts
    return state


def node_generate_answer(state: RAGState) -> RAGState:
    ans = generate_answer(
        question=state["question"],
        pages=state.get("pages", []),
        facts=state.get("facts", []),
    )
    state["answer"] = ans
    return state


def build_graph():
    builder = StateGraph(RAGState)

    builder.add_node("retrieve_pages", node_retrieve_pages)
    builder.add_node("query_graph", node_query_graph)
    builder.add_node("generate_answer", node_generate_answer)

    # simple linear flow; baad me branching add kar sakte
    builder.add_edge(START, "retrieve_pages")
    builder.add_edge("retrieve_pages", "query_graph")
    builder.add_edge("query_graph", "generate_answer")
    builder.add_edge("generate_answer", END)

    return builder.compile()


graph = build_graph()


def run_rag(question: str) -> str:
    out = graph.invoke({"question": question, "pages": [], "facts": [], "answer": ""})
    return out["answer"]
