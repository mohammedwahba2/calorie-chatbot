from __future__ import annotations

import httpx

AUTH_URL = "http://127.0.0.1:8004/me"
NLP_URL = "http://127.0.0.1:8002/parse"
RECOMMEND_URL = "http://127.0.0.1:8003/recommend"


def call_auth_me(token: str) -> dict:
    with httpx.Client(timeout=20) as client:
        res = client.get(AUTH_URL, headers={"Authorization": f"Bearer {token}"})
        res.raise_for_status()
        return res.json()


def call_nlp_service(message: str) -> dict:
    with httpx.Client(timeout=20) as client:
        res = client.post(NLP_URL, json={"message": message})
        res.raise_for_status()
        return res.json()


def call_recommendation_service(user_data: dict) -> dict:
    with httpx.Client(timeout=20) as client:
        res = client.post(RECOMMEND_URL, json=user_data)
        res.raise_for_status()
        return res.json()
