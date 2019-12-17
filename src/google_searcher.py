import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import stanfordnlp
from clue import Clue
from guess import Guess
import re
from time import sleep

google_cache = {}

def search_google(clue:str):
    
    outtext = []
    url = "https://google.com/search"
    page = requests.get(url,params={"q":clue},headers={"user-agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content,features='html5lib') 

    for script in soup(["script","style"]):
        script.decompose()

    for s in soup.find_all("div",{"class":["BNeawe s3v9rd AP7Wnd","BNeawe deIvCb AP7Wnd","BNeawe vvjwJb AP7Wnd"]},text=True):
        if "·" not in s.text:
            outtext.append(clean_result(s.text))
    
    google_cache[clue] = outtext
    sleep(1)
   
    return outtext

def clean_result(result:str):
    result = result.lower()
    result.replace(u'\xa0', u' ').replace(", ...",". ").replace(" ...",". ").replace("...",". ")
    result = ''.join(c for c in result if c.isalpha() or c == " ")

    return result


def get_blank_answers(clue:Clue,limit=10,words_only=True):
    """Searches google for answers to fill in the blank questions."""
    
    if clue not in google_cache.keys():
        # quote wrap and google
        q = '"{}"'.format(clue.get_description().lower())
        results = " ".join(i for i in search_google(q))

        # regex search only for the words immediately before and after the blank
        q_split = q.split(" ")
        q_around_blank = " ".join([q_split[q_split.index("*")-1],"*",q_split[q_split.index("*")+1]])
        regex = q_around_blank.replace("*",".{{{}}}".format(clue.get_length())).strip('"')
        r = re.compile(regex)

        matches = re.findall(r,results)
        words = []
        for match in matches:
            for word in match.split(" "):
                if word.lower() not in regex.split(" "):
                    words.append(word)
        scores = score_words(words)
        ret = [Guess(clue, word, score) for word, score in scores]
        google_cache[clue] = ret
        return ret
    else:
        return google_cache[clue]

def get_quote_answers(clue:Clue,limit=10,words_only=True):
    #TODO google quote, use nlp to get answer

    return ["random","words"]

def word_counts(word_list):
    counts = {}
    for word in word_list:
        if word in counts.keys():
            counts[word] += 1
        else:
            counts[word] = 1
    
    return counts

def score_words(word_list):
    score_tuples = []
    counts = word_counts(word_list)
    for word in counts.keys():
        score_tuples.append((word,counts[word] * 25000))
    return sorted(score_tuples,key=lambda x: x[1],reverse=True)





