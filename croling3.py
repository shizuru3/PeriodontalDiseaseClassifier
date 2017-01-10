from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

# 任意のWikipediaページを取り出して、そのページのリンクのリストを作成する
# 対象としていないものを除外し目的の項目のリンクだけを取り出す
# 乱数生成期のシードを現在のシステムの時刻で設定し、ランダムな経路を取得する

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html,"lxml")
    return  bsObj.find("div",{"id":"bodyContent"}).findAll("a",href = re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0,len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
