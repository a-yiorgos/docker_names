import os
from fastapi.testclient import TestClient
from main import app
from names import ADJECTIVES, SURNAMES

client = TestClient(app)

def test_get_name():
    response = client.get("/name")
    assert response.status_code == 200
    data = response.json()
    assert "n" in data
    assert "name" in data
    assert "hostname" in data
    assert "timestamp" in data

    parts = data["name"].split("_")
    assert len(parts) == 2
    assert parts[0] in ADJECTIVES
    assert parts[1] in SURNAMES

def test_get_name_single_word_adjective():
    adj = ADJECTIVES[0]
    response = client.get(f"/name/{adj}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    parts = data["name"].split("_")
    assert parts[0] == adj
    assert parts[1] in SURNAMES

def test_get_name_single_word_surname():
    sur = SURNAMES[0]
    response = client.get(f"/name/{sur}")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    parts = data["name"].split("_")
    assert parts[0] in ADJECTIVES
    assert parts[1] == sur

def test_get_name_single_word_invalid():
    response = client.get("/name/invalidnonexistentword")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_get_name_combination_valid():
    valid_combo = f"{ADJECTIVES[0]}_{SURNAMES[0]}"
    response = client.get(f"/name/{valid_combo}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["name"] == valid_combo

def test_get_name_combination_invalid():
    response = client.get("/name/invalid_combo")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_boring_wozniak_default_denied(monkeypatch):
    monkeypatch.delenv("BORING_WOZNIAK", raising=False)

    # Check foo_bar check
    response = client.get("/name/boring_wozniak")
    assert response.status_code == 404

    # Check single word check for boring or wozniak
    # It should never generate boring_wozniak
    for _ in range(50):
        res_adj = client.get("/name/boring")
        assert res_adj.status_code == 200
        assert res_adj.json()["name"] != "boring_wozniak"

        res_sur = client.get("/name/wozniak")
        assert res_sur.status_code == 200
        assert res_sur.json()["name"] != "boring_wozniak"

def test_boring_wozniak_allowed(monkeypatch):
    monkeypatch.setenv("BORING_WOZNIAK", "allow")

    response = client.get("/name/boring_wozniak")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["name"] == "boring_wozniak"
