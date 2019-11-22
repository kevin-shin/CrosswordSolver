import requests
from clue import Clue

DATAMUSE_URL = "https://api.datamuse.com/words"


def get_answers(clue:Clue, words_only=True):
    """Takes in a Clue object and returns a list of words (optionally associated with scores) which
        are potential answers to the given clue."""
        
    return ["apple","orange","banana","celestial","artificial","intelligence"]

def request(params:dict):
    r = requests.get(DATAMUSE_URL,params)
    return r.json()

def clean_results(result_list, words_only=True):
    results = []
    for item in result_list:
        if words_only:
            results.append(item["word"])
        else:
            results.append((item["word"],item["score"]))
    return results


if __name__ == "__main__":
    words = request({"ml":"test","sp":"????"})
    print(clean_results(words))