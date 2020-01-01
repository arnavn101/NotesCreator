# importing modules
import nltk
import numpy as np
import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import HashingVectorizer
from operator import itemgetter 
from nltk.cluster.util import cosine_distance

class Summarizer():

    # Assigning variables and executing program
    def __init__(self, file_name, points):
        self.article_text = ""
        self.formatted_article_text = ""
        self.file_name = file_name
        self.summary_finale = ""
        self.basic_sentences = ""
        self.read_article()
        self.retrieve_summary(points)
        print(self.return_summary())

    # Parsing the text file
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
    
    # create vector representations of sentence
    def create_sentence_vectors(self):
        self.vectorizer = HashingVectorizer(norm = None, n_features = 17)
        self.removed_length_list = 0
        sentence_vectors = []
        for sentence in self.formatted_article_text:
            if len(sentence) !=0:
                to_be_vectorized = [sentence]
                vectors = (self.vectorizer.fit_transform(to_be_vectorized)).toarray()
            else:
                continue
            sentence_vectors.append(vectors)
        return sentence_vectors

    # retrieve the similarity between two sentence vectors
    def sentence_similarity_calculator(self, vectorized_sentence_1, vectorized_sentence_2):
        return 1 - cosine_distance(vectorized_sentence_1, vectorized_sentence_2)

    # create similarity matrix containing all sentences in the text
    def create_similarity_matrix(self, sentence_vectors):
        similarity_matrix = np.zeros((len(self.basic_sentences), len(self.basic_sentences)))
        try:
            for x in range(len(self.basic_sentences)):
                for y in range(len(self.basic_sentences)):
                    if x != y:
                        similarity_matrix[x][y] = self.sentence_similarity_calculator(sentence_vectors[x][0], sentence_vectors[y][0])
        except IndexError:
            pass
        return similarity_matrix

    # Creating sentences and scoring them based on similarity to other sentences (source : nlpforhackers.io)
    def page_rank_algorithm(self, similarity_matrix, epochs=100, damping_factor=0.85, diff=0.0001):
        probability = np.ones(len(similarity_matrix)) / len(similarity_matrix)
        for x in range(epochs):
            new_probability = np.ones(len(similarity_matrix)) * (1 - damping_factor) / len(similarity_matrix) + damping_factor * similarity_matrix.T.dot(probability)
            change_in_probability = abs(new_probability - probability).sum()
            if change_in_probability <= diff:
                return new_probability
            probability = new_probability
        return probability

    # creating the overall summary of the text
    def finalize_summary(self, points):
        nltk.download('stopwords')
        nltk.download('punkt')

        self.formatted_article_text = [self.remove_stopwords(r.split()) for r in self.formatted_article_text]
        sentence_vectors = self.create_sentence_vectors()
        similarity_matrix = self.create_similarity_matrix(sentence_vectors)
        ranks_sentences = self.page_rank_algorithm(similarity_matrix)

        # indexes of sentences with their "pagerank" values
        index_sentences = sorted(enumerate(ranks_sentences))

        # sort list from greatest pagerank values to least
        index_sentences.sort(key=itemgetter(1), reverse=True)

        # use the indexes of sentences to get actual sentences
        selected_sentences = (list(zip(*index_sentences))[0][:points])
        summary_finale = []

        for element in selected_sentences:
            summary_finale.append(self.basic_sentences[element])
        return summary_finale    

    # Writing summary to file
    def write_summary(self, file_name, summary):
        with open("finale.txt", "w+") as myfile:
            myfile.write(summary)
        self.summary_finale = summary

    # finalizing output of sentences
    def retrieve_summary(self, points):
        for sentence in self.finalize_summary(points):
            self.summary_finale += "\n\n" + (''.join(sentence)).strip()
        
    # returning summary
    def return_summary(self):
        return self.summary_finale
