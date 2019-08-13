import bs4 as bs
import urllib.request
import re

def scrape_web(link):
    scraped_data = urllib.request.urlopen(link)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text
    
    with open("text.txt", "w+") as myfile:
        myfile.write(article_text)
scrape_web('https://en.wikipedia.org/wiki/Artificial_intelligence')