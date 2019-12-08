import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import stanfordnlp
from clue import Clue
import re

def google_answers(clue:str):
    
    url = "https://google.com/search"
    print(url)
    page = requests.get(url,params={"q":clue},headers={"user-agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content,features='html5lib') 

    outtext = []

    for script in soup(["script","style"]):
        script.decompose()

    with open("google.html","w",encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    for s in soup.find_all("div",{"class":["BNeawe s3v9rd AP7Wnd","BNeawe deIvCb AP7Wnd","BNeawe vvjwJb AP7Wnd"]},text=True):
        if "·" not in s.text:
            outtext.append(s.text.replace(u'\xa0', u' ')
            .replace(", ...",".")
            .replace(" ...",".")
            .replace("...","."))
    return outtext

def solve_blank(clue:Clue):
    q = clue.description.lower()
    results = " ".join(i for i in google_answers(clue.description))
    q = q.replace("*",".{{{}}}".format(clue.length))
    print(q)
    r = re.compile(q.replace("*",".{clue.length}"))

    matches = re.findall(r,results)
    print("MATCHES",matches)

    ret = [word for match in matches for word in match.split(" ") if word.lower() not in q.split(" ")]

    return ret

if __name__ == "__main__":
    c = Clue(0,0,5,"A","What a * of work is man",1)
    c = Clue(0,0,6,"A",'"Oh, what a * it is!"',1)
    print(solve_blank(c))
    print(google_answers('"Oh what a * it is"'))
    #stanfordnlp.download("en")
    # nlp = stanfordnlp.Pipeline()
    # doc = nlp(google_answers('"what a * * * is man"')[0])
    # doc.sentences[0].print_dependencies()
    
    





