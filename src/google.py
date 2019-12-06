import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import stanfordnlp

def google_answers(clue:str):
    url = "https://google.com/search"
    print(url)
    page = requests.get(url,params={"q":clue},headers={"user-agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content,features='html5lib') 

    outtext = []

    for script in soup(["script","style"]):
        script.decompose()

    # with open("google.html","w",encoding="utf-8") as f:
    #     f.write(str(soup.prettify()))

    for s in soup.find_all("div",{"class":"BNeawe s3v9rd AP7Wnd"},text=True):
        if "·" not in s.text:
            outtext.append(s.text.replace(u'\xa0', u' ')
            .replace(", ...",".")
            .replace(" ...",".")
            .replace("...","."))

    return outtext

if __name__ == "__main__":
    print(google_answers('"what a * * * is man"'))
    #stanfordnlp.download("en")
    # nlp = stanfordnlp.Pipeline()
    # doc = nlp(google_answers('"what a * * * is man"')[0])
    # doc.sentences[0].print_dependencies()
    
    





