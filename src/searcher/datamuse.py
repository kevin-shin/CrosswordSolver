import requests
from clue import Clue
from guess import Guess

DATAMUSE_URL = "https://api.datamuse.com/words"
verbose = True

def get_answers(clue:Clue, limit = 10, words_only=True):
    """Takes in a Clue object and returns a list of words (optionally associated with scores) which
        are potential answers to the given clue."""
    params = {}
    length = clue.get_length()

    params["ml"] = clue.description
    params["sp"] = "?" * clue.length

    results = clean_results(clue, request(params),words_only=words_only)[:limit]

    return results

def request(params:dict):
    r = requests.get(DATAMUSE_URL,params)
    try:
        return r.json()
    except:
        print(r.json())
        return "{{}}"


def clean_results(clue, result_list, words_only=True):
    results = []
    for item in result_list:
        if words_only:
            guess = Guess(clue, item["word"], item["score"])
            results.append(guess)
        else:
            pass
            # results.append((item["word"],item["score"]))
    return results
