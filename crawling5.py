from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# ページですぐ見つかったすべての内部リンクのリストを取り出す
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    # "/" で始まるすべてのリンクを見つける
    for link in bsObj.findAll("a", href = re.compile("^(\/|.*" + includeUrl +")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return  internalLinks

# ページで見つかったすべての外部リンクのリストを返す
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 現在のURLを含まない"http"か"www"で始まるすべてのリンクを見つける
    for link in bsObj.findAll("a", href = re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExtenalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html, "lxml")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, loocking around the site for one")
        domain = (urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc)
        internalLinks = getInternalLinks(bsObj, startingPage)
        return getRandomExtenalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExtenalLink(startingSite)
    print("Random external link is:" + externalLink)
    followExternalOnly(externalLink)

# このサイトで見つかったすべての外部URLのリストを集める
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    domain = urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc
    bsObj = BeautifulSoup(html,"lxml")
    internalLinks = getInternalLinks(bsObj,domain)
    externalLinks = getExternalLinks(bsObj,domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)

allIntLinks.add("http://oreilly.com")
getAllExternalLinks("http://oreilly.com")