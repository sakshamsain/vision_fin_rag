import networkx as nx
from typing import List
from .models import GraphFact

G = nx.DiGraph()

def add_fact(f: GraphFact):
    subj = f.subject
    obj = f.obj
    G.add_node(subj)
    G.add_node(obj)
    G.add_edge(subj, obj, relation=f.relation, value=f.value, year=f.year)

def get_revenue(company: str, year: int) -> List[GraphFact]:
    facts = []
    for u, v, data in G.edges(data=True):
        if u.lower() == company.lower() and data.get("relation") == "revenue" and data.get("year") == year:
            facts.append(
                GraphFact(
                    subject=u,
                    relation=data["relation"],
                    obj=v,
                    value=data.get("value"),
                    year=data.get("year"),
                )
            )
    return facts

def get_all_facts_for_company(company: str) -> List[GraphFact]:
    facts = []
    for u, v, data in G.edges(data=True):
        if u.lower() == company.lower():
            facts.append(
                GraphFact(
                    subject=u,
                    relation=data.get("relation", ""),
                    obj=v,
                    value=data.get("value"),
                    year=data.get("year"),
                )
            )
    return facts
