# app/workflow.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from .retrieval import retrieve_pages  # tu jo function use karta
from .graph_store import get_facts_for_question
from .llm import generate_answer  # tera LLM wrapper

class RAGState(TypedDict):
    question: str
    pages: List[str]
    facts: List[str]
    answer: str

def node_retrieve_pages(state: RAGState) -> RAGState:
    state["pages"] = retrieve_pages(state["question"])
    return state

def node_query_graph(state: RAGState) -> RAGState:
    state["facts"] = get_facts_for_question(state["question"])
    return state

def node_generate_answer(state: RAGState) -> RAGState:
    state["answer"] = generate_answer(
        question=state["question"],
        pages=state.get("pages", []),
        facts=state.get("facts", []),
    )
    return state

def build_graph():
    g = StateGraph(RAGState)
    g.add_node("retrieve_pages", node_retrieve_pages)
    g.add_node("query_graph", node_query_graph)
    g.add_node("generate_answer", node_generate_answer)
    g.add_edge(START, "retrieve_pages")
    g.add_edge("retrieve_pages", "query_graph")
    g.add_edge("query_graph", "generate_answer")
    g.add_edge("generate_answer", END)
    return g.compile()

graph = build_graph()

def run_rag(question: str) -> str:
    out = graph.invoke({"question": question, "pages": [], "facts": [], "answer": ""})
    return out["answer"]
