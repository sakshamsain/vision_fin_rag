import requests
from .config import LLM_API_URL, LLM_MODEL_NAME
from .models import RetrievedPage, GraphFact

def build_prompt(question: str, pages: list[RetrievedPage], facts: list[GraphFact]) -> str:
    lines = []
    lines.append("You are a financial analyst. Answer using only the context.")
    lines.append("")
    lines.append("Question:")
    lines.append(question)
    lines.append("")
    if facts:
        lines.append("Structured facts:")
        for f in facts:
            line = f"- {f.subject} {f.relation} {f.obj}"
            if f.value is not None:
                line += f" value={f.value}"
            if f.year is not None:
                line += f" year={f.year}"
            lines.append(line)
    if pages:
        lines.append("")
        lines.append("Retrieved pages (metadata only):")
        for p in pages:
            lines.append(f"- Company={p.company}, Year={p.year}, Page={p.page_num}")
    lines.append("")
    lines.append("Now provide a concise answer.")
    return "\n".join(lines)

def call_llm(prompt: str) -> str:
    # Example: Ollama-style REST call; change as per your LLM
    try:
        resp = requests.post(
            f"{LLM_API_URL}/api/generate",
            json={"model": LLM_MODEL_NAME, "prompt": prompt},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"LLM error: {e}"
