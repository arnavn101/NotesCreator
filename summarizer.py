# importing modules
import nltk
import numpy as np
import re
import heapq

class Summarizer():

# Assigning variables and executing program
    def __init__(self, file_name, points):
        self.article_text = ""
        self.formatted_article_text = ""
        self.word_frequencies = {}
        self.sentence_scores = {}
        self.file_name = file_name
        self.read_article()
        self.maximum_occurence()
        self.sentence_scoring()
        self.finalize_summary("finale.txt", points)

    # Parsing text file
    def read_article(self):
        with open(self.file_name, "r") as myfile:
            self.article_text = myfile.read()

        # Removing Square Brackets and Extra Spaces
        self.article_text = re.sub(r'\[[0-9]*\]', ' ', self.article_text)
        self.article_text = re.sub(r'\s+', ' ', self.article_text)

        # Removing special characters and digits
        self.formatted_article_text = re.sub('[^a-zA-Z]', ' ', self.article_text)
        self.formatted_article_text = re.sub(r'\s+', ' ', self.formatted_article_text)

    # Finding most important words in text
    def maximum_occurence(self):
        stopwords = nltk.corpus.stopwords.words('english')
        nltk.download('stopwords')
        nltk.download('punkt')
        
        self.word_frequencies = {}
        for word in nltk.word_tokenize(self.formatted_article_text):
            if word not in stopwords:
                if word not in self.word_frequencies.keys():
                    self.word_frequencies[word] = 1
                else:
                    self.word_frequencies[word] += 1

        maximum_frequency = max(self.word_frequencies.values())

        for word in self.word_frequencies.keys():
            self.word_frequencies[word] = (self.word_frequencies[word]/maximum_frequency)

    # Creating sentences and scoring them based on accuracy
    def sentence_scoring(self):
        sentence_list = nltk.sent_tokenize(self.article_text)
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in self.word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in self.sentence_scores.keys():
                            self.sentence_scores[sent] = self.word_frequencies[word]
                        else:
                            self.sentence_scores[sent] += self.word_frequencies[word]

    # retrieving summarized text
    def finalize_summary(self, file_name, points):
        summary_sentences = heapq.nlargest(points, self.sentence_scores, key=self.sentence_scores.get)
        summary = '\n'.join(summary_sentences)
        print(summary)

        self.write_summary(file_name, summary)
    
    # Writing summary to file
    def write_summary(self, file_name, summary):
        with open("finale.txt", "w+") as myfile:
            myfile.write(summary)
