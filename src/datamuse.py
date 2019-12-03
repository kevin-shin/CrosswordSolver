import requests
from clue import Clue
from guess import Guess

DATAMUSE_URL = "https://api.datamuse.com/words"
verbose = True

def get_answers(clue:Clue, limit = 10, words_only=True):
    """Takes in a Clue object and returns a list of words (optionally associated with scores) which
        are potential answers to the given clue."""
    params = {}
    length = clue.length
    parts = clue.description.split(" _ ",maxsplit=1)

    if len(parts) > 1:
        params['lc'] = parts[0].split(" ")[-1]
        if parts[1] != '':
            params['rc'] = parts[1].split(" ")[0]
    else:
        params["ml"] = clue.description
    
    params["sp"] = "?" * clue.length

    results = clean_results(clue, request(params),words_only=words_only)[:limit]

    return results

def request(params:dict):
    r = requests.get(DATAMUSE_URL,params)
    return r.json()

def clean_results(clue, result_list, words_only=True):
    results = []
    for item in result_list:
        if words_only:
            guess = Guess(clue, item["word"])
            results.append(guess)
        else:
            pass
            # results.append((item["word"],item["score"]))
    return results


# if __name__ == "__main__":
#     print(get_answers(Clue(0,0,5,"A","as american as _ pie",1)))