from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# 任意のWikipediaページを取り出して、そのページのリンクのリストを作成する
# 対象としていないものを除外し目的の項目のリンクだけを取り出す
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html,"lxml")

for link in bsObj.find("div",{"id":"bodyContent"}).findAll("a",href = re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
