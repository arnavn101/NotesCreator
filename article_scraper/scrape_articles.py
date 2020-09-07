import os
import sys
import nltk
import requests
import unicodedata
from itertools import groupby
from readability import Document
from article_scraper.strip_html import HTMLStripper

sys.path.insert(0, os.getcwd())  # Resolve Importing errors


class ArticleScraper:
    def __init__(self, website_name):
        self.text_content = ""
        self.separated_sentences = []
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.request_website = requests.get(website_name, headers=self.returnRandomHeaders()
                                            , timeout=10)
        self.retrieve_important()
        self.separate_sentences(self.text_content)
        self.strip_longSpaces()
        self.remove_escapeChars()

    def returnRandomHeaders(self):
        return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1", "DNT": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language":
                "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

    def strip_tags(self, html_content):
        html_stripper = HTMLStripper()
        html_stripper.feed(html_content)
        return html_stripper.get_data()

    def retrieve_important(self):
        article_content = Document(self.request_website.text)
        html_text = article_content.summary()
        self.text_content = (self.strip_tags(html_text))
        self.text_content = unicodedata.normalize("NFKD", self.text_content)

    def separate_sentences(self, text_article):
        self.separated_sentences = self.tokenizer.tokenize(text_article)

    def format_badSentences(self):
        index_sentence = 0
        for individual_sentence in self.separated_sentences:
            if "\n\n" in individual_sentence:
                self.separated_sentences[index_sentence] = (" ".join(individual_sentence.rsplit("\n\n", 1)[1:]))
            index_sentence += 1

    def remove_escapeChars(self):
        self.format_badSentences()
        self.separated_sentences = [individual_sentence.replace('\n', '').strip() for individual_sentence
                                    in self.separated_sentences]

    def return_article(self):
        return ' '.join(individual_sentence for individual_sentence in self.separated_sentences)

    def strip_longSpaces(self, max_specified=5):
        for individual_sentence in self.separated_sentences:
            current_max = 0

            # First, break the string up into individual strings for each space
            split_string = individual_sentence.split(" ")

            # Iterate over the list returning each string
            for c, sub_group in groupby(split_string):
                if c != '':
                    continue

                # Get the length of the run of spaces
                i = len(list(sub_group))

                if i > current_max:
                    current_max = i

            if current_max > max_specified:
                self.separated_sentences.remove(individual_sentence)
