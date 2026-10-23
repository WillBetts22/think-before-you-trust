"""
prompts.py — every prompt the experiment sends, plus the helpers that turn
MuSiQue decompositions into askable questions.

Direct and stepwise routes share the same system prompt, the same evidence
block and the same answer format, so the only thing that differs between
routes is the composition itself.
"""

from __future__ import annotations

import re

import config

SYSTEM = (
    "You answer factual questions. Be concise: give the shortest answer that "
    "fully answers the question (usually an entity name, date or number). "
    "Respond with JSON only."
)

ANSWER_FORMAT = (
    'Respond with JSON only: {"answer": "<short answer, or \\"unknown\\" if you cannot answer>"}'
)

ORIGINAL_FORMAT = (
    "Answer the question. Also give your answer to each step, in order, where "
    "#k refers to your answer to step k. Then give your confidence (0-100) that "
    "the final answer is correct.\n"
    'Respond with JSON only: {"intermediate_answers": ["<step 1>", "<step 2>", ...], '
    '"final_answer": "<short answer>", "confidence": <0-100>}'
)

_KB_HOP = re.compile(r"^\s*(.+?)\s*>>\s*(.+?)\s*$")
_REF = re.compile(r"#(\d+)")


def render_step(raw: str) -> str:
    """Turn a MuSiQue sub-question into natural language.

    Many hops are Wikidata-style 'Subject >> relation' strings; those become
    "What is the <relation> of <Subject>?". Natural-language hops pass through.
    Placeholders like #1 are kept. Rendered steps are listed in the audit
    sheet so awkward ones can be fixed or excluded by hand.
    """
    m = _KB_HOP.match(raw)
    if m:
        subj, rel = m.group(1), m.group(2)
        q = f"What is the {rel} of {subj}?"
    else:
        q = raw.strip()
        if not q.endswith("?"):
            q += "?"
    return q[0].upper() + q[1:]


def refs(step: str) -> set[int]:
    return {int(n) for n in _REF.findall(step)}


def fill(step: str, answers: dict[int, str]) -> str:
    """Substitute #k with the given (model-generated) answers."""
    return _REF.sub(lambda m: answers.get(int(m.group(1)), m.group(0)), step)


def compose(outer: str, inner: str, ref: int) -> str:
    """Build the composite question outer∘inner by nesting inner inside outer.

    Used only for sub-regions of longer chains, where MuSiQue has no
    human-written composite question. For a whole chain, the original
    MuSiQue question is used instead.
    """
    return outer.replace(f"#{ref}", f'(the answer to "{inner.rstrip("?")}")')


def evidence_block(paragraphs: list[dict]) -> str:
    if config.CONDITION != "open_book":
        return ""
    lines = [f"[{i + 1}] {p['title']}: {p['text']}" for i, p in enumerate(paragraphs)]
    return "Use these documents (some are irrelevant):\n" + "\n\n".join(lines) + "\n\n"


def answer_prompt(question: str, paragraphs: list[dict]) -> str:
    return f"{evidence_block(paragraphs)}Question: {question}\n\n{ANSWER_FORMAT}"


def original_prompt(question: str, steps: list[str], paragraphs: list[dict]) -> str:
    step_lines = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
    return (f"{evidence_block(paragraphs)}Question: {question}\n\nSteps:\n{step_lines}\n\n"
            f"{ORIGINAL_FORMAT}")
