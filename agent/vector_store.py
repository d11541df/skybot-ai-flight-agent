"""OpenAI Embeddings 기반 항공사 정책 RAG (경량 구현)"""

import json
import os
import numpy as np
from openai import OpenAI
from langchain_core.tools import tool
from config import OPENAI_API_KEY

POLICIES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "airline_policies.json")

_store = None


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_store():
    global _store
    if _store is not None:
        return _store

    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(POLICIES_PATH, "r", encoding="utf-8") as f:
        policies = json.load(f)

    texts = [p["content"] for p in policies]
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small",
    )

    _store = {
        "policies": policies,
        "embeddings": [item.embedding for item in response.data],
        "client": client,
    }
    return _store


@tool
def search_airline_policy(query: str) -> str:
    """항공사 정책, 수하물 규정, 마일리지 등에 대해 검색합니다.

    Args:
        query: 검색할 질문 (예: 수하물 무게 제한, 마일리지 적립)
    """
    store = get_store()

    query_resp = store["client"].embeddings.create(
        input=[query],
        model="text-embedding-3-small",
    )
    query_emb = query_resp.data[0].embedding

    scores = [
        cosine_similarity(query_emb, emb)
        for emb in store["embeddings"]
    ]

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]

    response_parts = ["**관련 정책 안내:**\n"]
    for idx in top_indices:
        p = store["policies"][idx]
        sim = scores[idx]
        response_parts.append(
            f"**[{p['category']}] {p['title']}** (유사도: {sim:.2f})\n{p['content']}\n"
        )

    return "\n".join(response_parts)
