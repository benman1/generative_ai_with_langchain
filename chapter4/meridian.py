"""Shared helpers for the Meridian travel assistant.

Non-teaching utilities only: corpus loading, the evaluation set, and retrieval
metrics. The RAG components the chapter teaches (the two-level index, RRF, the
assembled retriever, the assistant graph) live in the notebook cells, because
those are the listings the book shows.

Pure Python plus numpy, so this imports and runs without downloading a model.
"""

from __future__ import annotations

import json
import os
import re
from typing import Callable, Iterable

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "meridian")


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the `key: value` frontmatter each corpus file starts with."""
    if not text.startswith("---"):
        return {}, text
    _, frontmatter, body = text.split("---", 2)
    meta: dict = {}
    for line in frontmatter.strip().splitlines():
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        meta[key] = value == "true" if value in ("true", "false") else value
    return meta, body.strip()


def load_corpus(data_dir: str = DATA) -> list[dict]:
    """Load every corpus document as {doc_id, text, **metadata}."""
    docs = []
    for folder in ("destinations", "policies"):
        folder_path = os.path.join(data_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for name in sorted(os.listdir(folder_path)):
            if not name.endswith(".md"):
                continue
            with open(os.path.join(folder_path, name), encoding="utf-8") as handle:
                meta, body = _parse_frontmatter(handle.read())
            meta.setdefault("doc_id", name[:-3])
            docs.append({**meta, "text": body})
    return docs


def load_eval_set(data_dir: str = DATA) -> list[dict]:
    """Load the question set: question, gold_answer, gold_doc_ids, query_type."""
    with open(os.path.join(data_dir, "eval_set.json"), encoding="utf-8") as handle:
        return json.load(handle)


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def split_sentences(text: str) -> list[str]:
    """Split on sentence boundaries, keeping the punctuation."""
    return [s.strip() for s in SENTENCE_BOUNDARY.split(text.strip()) if s.strip()]


def summarise(text: str, max_sentences: int = 3, max_chars: int = 500) -> str:
    """A section's stand-in for itself at the coarse level of the index.

    The first few sentences of a well-written section say what it is about,
    which is all level one has to get right.
    """
    summary = " ".join(split_sentences(text)[:max_sentences])
    return summary if len(summary) <= max_chars else summary[:max_chars] + "..."


def estimate_tokens(text: str) -> int:
    """Rough token count. Four characters per token is close enough to budget."""
    return len(text) // 4


# ---------------------------------------------------------------------------
# Retrieval metrics
# ---------------------------------------------------------------------------

def recall_at_k(ranked_ids: list[str], gold_ids: Iterable[str], k: int) -> float:
    """Fraction of the gold documents that appear in the top k."""
    gold = set(gold_ids)
    if not gold:
        return 0.0
    return len(gold & set(ranked_ids[:k])) / len(gold)


def hit_at_k(ranked_ids: list[str], gold_ids: Iterable[str], k: int) -> float:
    """1.0 if any gold document appears in the top k."""
    return 1.0 if set(gold_ids) & set(ranked_ids[:k]) else 0.0


def reciprocal_rank(ranked_ids: list[str], gold_ids: Iterable[str]) -> float:
    """1 / rank of the first gold document, or 0 if none appears."""
    gold = set(gold_ids)
    for position, doc_id in enumerate(ranked_ids, start=1):
        if doc_id in gold:
            return 1.0 / position
    return 0.0


def ndcg_at_k(ranked_ids: list[str], gold_ids: Iterable[str], k: int) -> float:
    """Normalised discounted cumulative gain with binary relevance."""
    gold = set(gold_ids)
    gains = [1.0 if doc_id in gold else 0.0 for doc_id in ranked_ids[:k]]
    dcg = sum(g / np.log2(i + 2) for i, g in enumerate(gains))
    ideal = sum(1.0 / np.log2(i + 2) for i in range(min(len(gold), k)))
    return dcg / ideal if ideal else 0.0


def evaluate_retriever(
    retrieve: Callable[[str], list[str]],
    eval_set: list[dict],
    k: int = 5,
) -> dict[str, float]:
    """Average Recall@k, Hit@k, MRR and nDCG@k over the evaluation set.

    `retrieve` takes a question and returns document ids, best first.
    """
    scores = {f"recall@{k}": [], f"hit@{k}": [], "mrr": [], f"ndcg@{k}": []}
    for item in eval_set:
        ranked = retrieve(item["question"])
        gold = item["gold_doc_ids"]
        scores[f"recall@{k}"].append(recall_at_k(ranked, gold, k))
        scores[f"hit@{k}"].append(hit_at_k(ranked, gold, k))
        scores["mrr"].append(reciprocal_rank(ranked, gold))
        scores[f"ndcg@{k}"].append(ndcg_at_k(ranked, gold, k))
    return {name: float(np.mean(values)) for name, values in scores.items()}
