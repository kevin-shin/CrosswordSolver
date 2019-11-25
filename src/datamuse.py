import requests
from clue import Clue

DATAMUSE_URL = "https://api.datamuse.com/words"


def get_answers(clue:Clue, words_only=True):
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

    print(params)

    return clean_results(request(params),words_only=words_only)

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
    print(get_answers(Clue(0,0,5,"A","as american as _ pie",1)))