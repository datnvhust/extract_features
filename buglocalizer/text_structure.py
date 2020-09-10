
import pickle
import json
from math import log
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
"""
import en_vectors_web_lg

from sklearn.preprocessing import MinMaxScaler
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from tfidf import TFIDFVectorizer


def calculate_similarity(src_files, bug_reports):
    
    # nlp = en_vectors_web_lg.load()
    
    all_simis = []
    print(bug_reports)
    doc_list_summary = []
    tfidf = TFIDFVectorizer()
    for report in bug_reports.values():
        # report_doc = nlp(' '.join(report.summary['unstemmed']
        #                           + report.pos_tagged_description['unstemmed']))
        scores = []
        uniqueWords = set(report.summary['unstemmed'])
        doc = dict.fromkeys(uniqueWords, 0)
        # print(report.summary['unstemmed'])
        for word in report.summary['unstemmed']:
            doc[word] += 1
        doc_list_summary.append(doc)
        # summary = nlp(' '.join(report.summary['unstemmed']))
        # print(summary)
        # summary = tfidf.fit_transform(report.summary['unstemmed'])
        # print(summary)
        # description = nlp(' '.join(report.description['unstemmed']))
        # print(report.pos_tagged_summary['unstemmed'])
        # print(summary.similarity(description))
        for src in src_files.values():
            x = 0
            # class_names = nlp(' '.join(src.class_names['unstemmed']))
            # attributes = nlp(' '.join(src.attributes['unstemmed']))
            # comments = nlp(' '.join(src.comments['unstemmed']))
            # method_names = nlp(' '.join(src.method_names['unstemmed']))

            # simi = (
            #         summary.similarity(class_names)
            #         + summary.similarity(attributes)
            #         + summary.similarity(comments)
            #         + summary.similarity(method_names)
            #         + description.similarity(class_names)
            #         + description.similarity(attributes)
            #         + description.similarity(comments)
            #         + description.similarity(method_names))
            # scores.append(simi)
        
        all_simis.append(scores)
        # print(scores)
    print(doc_list_summary)
    for doc in doc_list_summary:
        for word in doc:
            print(tfidf.tfidf(word, doc, doc_list_summary))
    return all_simis
    """
class TFIDFVectorizer():
    def __init__(self, k=1.5, b=0.75):
        self.k = k
        self.b = b

    def tf(self,word,doc, doc_list):
        all_num=sum([doc[key] for key in doc])
        avg = 0
        for vb in doc_list:
            avg += sum([vb[key] for key in vb])
        avg = avg/len(doc_list)
        return (doc[word]*(self.k + 1))/(doc[word] + self.k*(1 - self.b + self.b*all_num/avg))

    def idf(self, word,doc_list):
        all_num=len(doc_list)
        word_count=0
        for doc in doc_list:
            if word in doc:
                word_count+=1
        return log((all_num+1)/(word_count+0.5))

    def tfidf(self, word,doc,doc_list):
        score = self.tf(word,doc, doc_list)*self.idf(word,doc_list)
        return score
    def compute_tfidf_summary(self, bug_reports):
        vocab = []
        docs = []
        for report in bug_reports.values():
            doc = {}
            for word in report.summary['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
                if word in doc.keys():
                    doc[word] += 1
                else:
                    doc[word] = 1
            docs.append(doc)
        x_tfidf = []
        for doc in docs:
            for word in doc:
                doc[word] = self.tfidf(word,doc,docs)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            x_tfidf.append(row)
        # should save sparse matrix
        return x_tfidf
    def compute_similarity(self, x_tfidf):
        """
        compute similarity
        """
        n = len(x_tfidf)
        size = len(x_tfidf[n-1])
        x_tfidf = np.asarray(x_tfidf)
        x_similarity = np.empty((n, n), dtype=object) 
        for i in range(n):
            for j in range(n):     
                x_similarity[i][j] = cosine_similarity(x_tfidf[i].reshape(1,size), x_tfidf[j].reshape(1,size))[0][0]
        return x_similarity

def main():
    
    with open('../preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open('../preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
        
    tf = TFIDFVectorizer()
    x = tf.compute_tfidf_summary(bug_reports)
    x = tf.compute_similarity(x)
    print(x)
  
if __name__ == '__main__':
    main()
