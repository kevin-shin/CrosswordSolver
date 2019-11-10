import requests

DATAMUSE_URL = "https://api.datamuse.com/words"


def request(params:dict):
    r = requests.get(DATAMUSE_URL,params)
    return r.json()


if __name__ == "__main__":
    words = request({"ml":"test","sp":"????"})
    print(words)
    print(words[0]["word"])
