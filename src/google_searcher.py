import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import stanfordnlp
from clue import Clue
from guess import Guess
import re

def search_google(clue:str):
    
    url = "https://google.com/search"
    page = requests.get(url,params={"q":clue},headers={"user-agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content,features='html5lib') 

    outtext = []

    for script in soup(["script","style"]):
        script.decompose()

    with open("google.html","w",encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    for s in soup.find_all("div",{"class":["BNeawe s3v9rd AP7Wnd","BNeawe deIvCb AP7Wnd","BNeawe vvjwJb AP7Wnd"]},text=True):
        if "·" not in s.text:
            outtext.append(clean_result(s.text))
    return outtext

def clean_result(result:str):
    result = result.lower()
    result.replace(u'\xa0', u' ').replace(", ...",". ").replace(" ...",". ").replace("...",". ")
    result = ''.join(c for c in result if c.isalpha() or c == " ")

    return result


def get_blank_answers(clue:Clue,limit=10,words_only=True):
    """Searches google for answers to fill in the blank questions."""
    
    # quote wrap and google
    q = '"{}"'.format(clue.get_description().lower())
    results = " ".join(i for i in search_google(q))

    # regex search only for the words immediately before and after the blank
    q_split = q.split(" ")
    q_around_blank = " ".join([q_split[q_split.index("*")-1],"*",q_split[q_split.index("*")+1]])
    q = q_around_blank.replace("*",".{{{}}}".format(clue.get_length())).strip('"')

    r = re.compile(q)

    matches = re.findall(r,results)

    ret = [Guess(clue, word, 10000000) for match in matches for word in match.split(" ") if word.lower() not in q.split(" ")]

    return ret

def get_quote_answers(clue:Clue,limit=10,words_only=True):
    #TODO google quote, use nlp to get answer

    return ["random","words"]

if __name__ == "__main__":
    c = Clue(0,0,5,"A","What a * of work is man",1)
    c = Clue(0,0,6,"A",'"oh what a * it is"',1)
    c = Clue(0,0,4,"A",'"from * to nuts"',1)
    print(get_blank_answers(c))
    #print(search_google('"Oh, What a * It Is!"'))
    
    #stanfordnlp.download("en")
    # nlp = stanfordnlp.Pipeline()
    # doc = nlp("Freudian focus")
    # doc.sentences[0].print_dependencies()
    
    





