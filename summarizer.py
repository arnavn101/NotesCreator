import nltk
import numpy as np
import re
import heapq

def read_article(file_name):
    with open(file_name, "r") as myfile:
        article_text = myfile.read()

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    return article_text, formatted_article_text

def maximum_occurence(formatted_article_text):
    stopwords = nltk.corpus.stopwords.words('english')
    
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    return word_frequencies

def sentence_scoring(article_text, word_frequencies):
    sentence_scores = {}
    sentence_list = nltk.sent_tokenize(article_text)

    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    return sentence_scores

def get_summary(file_name):
    article_text, formatted_article_text = read_article(file_name)
    word_frequencies = maximum_occurence(formatted_article_text)
    sentence_scores = sentence_scoring(article_text, word_frequencies)

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = '\n'.join(summary_sentences)
    print(summary)
    
    with open("finale.txt", "w+") as myfile:
        myfile.write(summary)

get_summary("text.txt")