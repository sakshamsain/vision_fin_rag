from typing import List
from .models import QueryRequest, AnswerResponse, RetrievedPage, GraphFact
from .embeddings import search_pages
from .graph_store import get_all_facts_for_company
from .llm import build_prompt, call_llm

def answer_question(req: QueryRequest) -> AnswerResponse:
    pages: List[RetrievedPage] = search_pages(req.question, company=req.company)
    facts: List[GraphFact] = []
    if req.company:
        facts = get_all_facts_for_company(req.company)

    prompt = build_prompt(req.question, pages, facts)
    ans = call_llm(prompt)
    return AnswerResponse(
        answer=ans,
        retrieved_pages=pages,
        graph_facts=facts,
    )
