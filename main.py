import os
import random
import socket
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

# Global counter
counter = 0

# Adjectives and Surnames from Moby/namesgenerator
ADJECTIVES = [
    "admiring", "adoring", "affectionate", "agitated", "amazing", "angry", 
    "awesome", "backstabbing", "berserk", "big", "boring", "clever", 
    "compassionate", "condescending", "cranky", "dazzling", "determined", 
    "distracted", "dreamy", "eager", "ecstatic", "elastic", "elated", 
    "elegant", "eloquent", "epic", "fervent", "festive", "flamboyant", 
    "focused", "friendly", "frosty", "funny", "gallant", "gifted", 
    "goofy", "gracious", "happy", "hardcore", "heuristic", "hopeful", 
    "hungry", "infallible", "inspiring", "jolly", "jovial", "keen", 
    "kind", "laughing", "loving", "lucid", "magical", "mystifying", 
    "modest", "musing", "naughty", "nervous", "nifty", "nostalgic", 
    "objective", "optimistic", "peaceful", "pedantic", "pensive", 
    "practical", "priceless", "quirky", "quizzical", "relaxed", 
    "reverent", "romantic", "sad", "serene", "sharp", "silly", 
    "sleepy", "stoic", "stupefied", "suspicious", "sweet", "tender", 
    "thirsty", "trusting", "unruffled", "upbeat", "vibrant", "vigorous", 
    "wizardly", "wonderful", "xenial", "youthful", "zealous", "zen"
]

SURNAMES = [
    "albattani", "allen", "almeida", "antonelli", "archimedes", "ardinghelli", 
    "aryabhata", "austin", "babbage", "banach", "bardeen", "bartik", "bassi", 
    "bell", "benz", "bhabha", "bhaskara", "blackwell", "bohr", "booth", 
    "borg", "bose", "boyd", "brahmagupta", "brattain", "brown", "burnell", 
    "cannon", "carson", "chandrasekhar", "chaplygin", "chatelet", "chatterjee", 
    "chebyshev", "cohen", "colden", "cori", "cray", "curie", "darwin", 
    "davinci", "dewdney", "dhawan", "diffie", "dijkstra", "dirac", "driscoll", 
    "dubinsky", "easley", "edison", "einstein", "elion", "engelbart", 
    "euclid", "euler", "fermat", "fermi", "feynman", "franklin", "galileo", 
    "galois", "ganguly", "gates", "gauss", "goldberg", "goldstine", "goodall", 
    "goldwasser", "gould", "greider", "grothendieck", "haibun", "hamilton", 
    "heisenberg", "hermann", "heyrovsky", "hodgkin", "hoover", "hopper", 
    "hugle", "hypatia", "ishizaka", "jackson", "jang", "jennings", "jepsen", 
    "johnson", "joliot", "jones", "kalam", "kapitsa", "kare", "keldysh", 
    "kepler", "khayyam", "khorana", "kilby", "kirch", "knuth", "kowalevski", 
    "lalande", "lamarr", "lamport", "leavitt", "lederberg", "lehmann", 
    "lewin", "liskov", "lovelace", "lumiere", "mahavira", "marconi", "meitner", 
    "mendel", "mendeleev", "mcclintock", "mclean", "minsky", "mirzakhani", 
    "montalcini", "moore", "morse", "murdock", "newton", "nightingale", 
    "noether", "northcutt", "noyce", "panini", "pare", "pasteur", "payne", 
    "perlman", "pike", "poincare", "polanyi", "poitras", "ptolemy", "raman", 
    "ramanujan", "ride", "ritchie", "roentgen", "rosalind", "saha", "sammet", 
    "sanderson", "satoshi", "shannon", "shaw", "shirley", "shockley", 
    "sinoussi", "snyder", "solomon", "spence", "stallman", "stonebraker", 
    "sutherland", "swanson", "swartz", "turing", "varahamihira", "visvesvaraya", 
    "volhard", "wescoff", "wilcox", "wiles", "williams", "williamson", 
    "wilson", "wozniak", "wright", "yalow", "yonath"
]

def generate_docker_name():
    global counter
    while True:
        adj = random.choice(ADJECTIVES)
        sur = random.choice(SURNAMES)
        name = f"{adj}_{sur}"
        
        # Check environment variable for "boring_wozniak" logic
        if name == "boring_wozniak":
            if os.getenv("BORING_WOZNIAK") == "allow":
                return name
            continue # Try again if not allowed
        return name

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
