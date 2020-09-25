
import pickle
import json
from math import log
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
from datasets import DATASET
from json import JSONEncoder

class TFIDFVectorizer():
    def __init__(self, k=1.5, b=0.75):
        self.k = k
        self.b = b

    def tf(self, word, doc, doc_list):
        all_num = sum([doc[key] for key in doc])
        avg = 0
        for vb in doc_list:
            avg += sum([vb[key] for key in vb])
        avg = avg/len(doc_list)
        return (doc[word]*(self.k + 1))/(doc[word] + self.k*(1 - self.b + self.b*all_num/avg))

    def idf(self, word, doc_list):
        all_num = len(doc_list)
        word_count = 0
        for doc in doc_list:
            if word in doc:
                word_count += 1
        return log((all_num+1)/(word_count+0.5))

    def tfidf(self, word, doc, doc_list):
        score = self.tf(word, doc, doc_list)*self.idf(word, doc_list)
        return score

    def compute_tfidf_summary(self, bug_reports, sources):
        vocab = []
        docs = []
        docs_report = []
        docs_source = []
        docs_summary = []
        docs_desc = []
        docs_class_name = []
        docs_method = []
        docs_atr = []
        docs_com = []
        for report in bug_reports.values():
            docs_report__ = {}
            data = report.summary['unstemmed'] +  report.description['unstemmed']
            for word in data:
                if word not in vocab:
                    vocab.append(word)

                if word in docs_report__.keys():
                    docs_report__[word] += 1
                else:
                    docs_report__[word] = 1
            
            docs_report.append(docs_report__)

        for src in sources.values():
            docs_source_ = {}
            data = src.file_name['unstemmed']  + src.attributes['unstemmed'] +  src.method_names['unstemmed'] + src.comments['unstemmed']
            for word in data:
                if word not in vocab:
                    vocab.append(word)
                if word in docs_source_.keys():
                    docs_source_[word] += 1
                else:
                    docs_source_[word] = 1
            # print(vocab)
            docs_source.append(docs_source_)

        x_tfidf = []
        for doc in docs_report:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_report)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            x_tfidf.append(row)
        print("x_tfidf")
        y_tfidf = []
        for doc in docs_source:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_source)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            y_tfidf.append(row)
        print("y_tfidf")

        return x_tfidf, y_tfidf


def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    tf = TFIDFVectorizer()
    x, y= tf.compute_tfidf_summary(bug_reports, src_files)
    print(len(x[0]))
    print(len(y[0]))
    with open(DATASET.root / 'report_tfidf.json', 'w') as file:
        json.dump(x, file)
    with open(DATASET.root / 'source_tfidf.json', 'w') as file:
        json.dump(y, file)



if __name__ == '__main__':
    main()
