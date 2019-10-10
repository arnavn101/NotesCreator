# importing modules
import nltk
import numpy as np
import re
import heapq
import pandas as pd
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

class Summarizer():

# Assigning variables and executing program
    def __init__(self, file_name, points):
        self.article_text = ""
        self.formatted_article_text = ""
        self.file_name = file_name
        self.summary_finale = ""
        self.basic_sentences = ""
        self.read_article()
        self.finalize_summary("finale.txt", points)

    # Parsing text file
    def read_article(self):
        with open(self.file_name, "r", encoding='utf-8') as myfile:
            self.article_text = myfile.read()

        # Removing Square Brackets and Extra Spaces
        self.article_text = re.sub(r'\[[0-9]*\]', ' ', self.article_text)
        self.article_text = re.sub(r'\s+', ' ', self.article_text)

        # Converting sentence into list
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.basic_sentences = tokenizer.tokenize(self.article_text)

        # Removing digits and periods in text
        self.formatted_article_text = pd.Series(self.basic_sentences).str.replace("[^a-zA-Z]", " ")

        # making alphabets lowercase
        self.formatted_article_text = [s.lower() for s in self.formatted_article_text]

    # remove common words from text
    def remove_stopwords(self, text):
        stop_words = stopwords.words('english')
        new_sentence = " ".join([i for i in text if i not in stop_words])
        return new_sentence

    def extract_wordVectors(self):
        word_embeddings = {}
        f = open('glove.6B.100d.txt', encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
        f.close()
        return word_embeddings

    def create_sentence_vectors(self, word_embeddings):
        sentence_vectors = []
        for i in self.formatted_article_text:
            if len(i) != 0:
                v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)
        return sentence_vectors

    def create_similarity_matrix(self, sentence_vectors):
        sim_mat = np.zeros([len(self.basic_sentences), len(self.basic_sentences)])

        for i in range(len(self.basic_sentences)):
            for j in range(len(self.basic_sentences)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
        return sim_mat
 
    # Creating sentences and scoring them based on accuracy
    def sentence_scoring(self, sim_mat):
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(self.basic_sentences)), reverse=True)
        return ranked_sentences

    # retrieving summarized text
    def finalize_summary(self, file_name, points):
        nltk.download('stopwords')
        nltk.download('punkt')

        self.formatted_article_text = [self.remove_stopwords(r.split()) for r in self.formatted_article_text]
        word_embeddings = self.extract_wordVectors()
        sentence_vectors = self.create_sentence_vectors(word_embeddings)
        sim_matrix = self.create_similarity_matrix(sentence_vectors)
        sentences_finale = self.sentence_scoring(sim_matrix)
        summary_final = ""

        for i in range(int(points)):
            if i > (len(sentences_finale)-1) :
                break
            print("\n\n" + sentences_finale[i][1])
            summary_final += "\n" + sentences_finale[i][1]

        self.write_summary(file_name, summary_final)
    
    # Writing summary to file
    def write_summary(self, file_name, summary):
        with open("finale.txt", "w+") as myfile:
            myfile.write(summary)
        self.summary_finale = summary

    def return_summary(self):
        return self.summary_finale


