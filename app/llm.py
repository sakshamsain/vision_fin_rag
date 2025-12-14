import requests
from .config import LLM_API_URL, LLM_MODEL_NAME, USE_EXTERNAL_LLM
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

def _offline_response(prompt: str) -> str:
    # Keep it deterministic and short to avoid surprises in UI
    preview = prompt.splitlines()
    preview = [line for line in preview if line.strip()]
    summary = "; ".join(preview[:3])
    if len(summary) > 300:
        summary = summary[:300] + "..."
    return f"[offline stub] {summary or 'No prompt content'}"


def call_llm(prompt: str) -> str:
    # If external LLM is disabled, use local stub
    if not USE_EXTERNAL_LLM:
        return _offline_response(prompt)

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
        # Fallback to offline stub but note the error for visibility
        return f"{_offline_response(prompt)} (LLM error: {e})"
