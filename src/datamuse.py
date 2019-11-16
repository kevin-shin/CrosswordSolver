import requests

DATAMUSE_URL = "https://api.datamuse.com/words"


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