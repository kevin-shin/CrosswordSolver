import requests
from clue import Clue
from guess import Guess

DATAMUSE_URL = "https://api.datamuse.com/words"
verbose = True

def get_answers(clue:Clue, limit = 10):
    """Takes in a Clue object and returns a list of words (optionally associated with scores) which
        are potential answers to the given clue."""

    params = {}
    length = clue.get_length()

    params["ml"] = clue.description
    params["sp"] = "?" * clue.length

    results = []
    for item in request(params)[:limit]:
        guess = Guess(clue, item["word"], item["score"])
        results.append(guess)

    return results

def request(params:dict):
    """Request a response from datamuse and return the JSON results"""

    r = requests.get(DATAMUSE_URL,params)
    try:
        return r.json()
    except:
        print(r.json())
        return "{{}}"

