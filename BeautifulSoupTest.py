from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://shizuru.hatenadiary.jp/entry/2017/01/08/001305")
bsObj = BeautifulSoup(html.read(),"lxml")
print(bsObj.h1)

