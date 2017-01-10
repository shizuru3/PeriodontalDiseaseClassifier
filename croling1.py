from urllib.request import urlopen
from bs4 import BeautifulSoup

# 任意のWikipediaページを取り出して、そのページのリンクのリストを作成する
# しかし、対象としていないものも含まれる
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html,"lxml")

for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
