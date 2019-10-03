import bs4 as bs
import urllib.request
import re

# Scrape text data from website
def scrape_web(file_name, link):
    scraped_data = urllib.request.urlopen(link)
    article = scraped_data.read()

    # parse paragraphs in article with lxml algorithm
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""
    for p in paragraphs:
        article_text += p.text

    write_file(file_name, article_text)
    
# Writing contents of response to file
def write_file(file_name, content):
	with open(file_name, 'w+', encoding='utf-8') as file:
        	file.write(content)

