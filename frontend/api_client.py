import requests

API_BASE = "http://localhost:8000"


def signup(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/signup", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()


def login(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()


def google_login(id_token: str):
    r = requests.post(f"{API_BASE}/auth/google", json={
        "id_token": id_token
    })
    r.raise_for_status()
    return r.json()


def get_me(id_token: str):
    r = requests.get(
        f"{API_BASE}/auth/me",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()


# FIX: Endpoint backend là /expenses/ (có dấu /)
def create_expense(id_token: str, data: dict):
    r = requests.post(
        f"{API_BASE}/expenses/",
        json=data,
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()


def get_expenses(id_token: str):
    r = requests.get(
        f"{API_BASE}/expenses/",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()