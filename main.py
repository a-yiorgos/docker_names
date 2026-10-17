import os
import random
import socket
from datetime import datetime
from fastapi import FastAPI, HTTPException
from names import ADJECTIVES, SURNAMES

app = FastAPI()

# Global counter
counter = 0

def is_boring_wozniak_allowed() -> bool:
    return os.getenv("BORING_WOZNIAK", "deny") == "allow"

def generate_docker_name() -> str:
    while True:
        adj = random.choice(ADJECTIVES)
        sur = random.choice(SURNAMES)
        name = f"{adj}_{sur}"
        if name == "boring_wozniak" and not is_boring_wozniak_allowed():
            continue
        return name

def is_valid_combination(adj: str, sur: str) -> bool:
    if adj not in ADJECTIVES or sur not in SURNAMES:
        return False
    if f"{adj}_{sur}" == "boring_wozniak" and not is_boring_wozniak_allowed():
        return False
    return True

@app.get("/name")
def get_name():
    global counter
    counter += 1
    return {
        "n": counter,
        "name": generate_docker_name(),
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/name/{name_param}")
def get_name_by_param(name_param: str):
    if "_" in name_param:
        adj, sur = name_param.split("_", 1)
        if is_valid_combination(adj, sur):
            return {"status": "OK", "name": name_param}
        else:
            raise HTTPException(status_code=404, detail="Invalid name combination")
    else:
        is_adj = name_param in ADJECTIVES
        is_sur = name_param in SURNAMES

        if not is_adj and not is_sur:
            raise HTTPException(status_code=404, detail="Name component not found")

        while True:
            if is_adj:
                sur = random.choice(SURNAMES)
                adj = name_param
            else:
                adj = random.choice(ADJECTIVES)
                sur = name_param

            combo = f"{adj}_{sur}"
            if combo == "boring_wozniak" and not is_boring_wozniak_allowed():
                continue
            return {"name": combo}
