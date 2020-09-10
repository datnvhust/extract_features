
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
        docs_summary = []
        docs_desc = []
        docs_class_name = []
        docs_method = []
        docs_atr = []
        docs_com = []
        # new_docs = []
        for report in bug_reports.values():
            doc = {}
            docs_summary__ = {}
            for word in report.summary['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
            # print(doc)
            # docs.append(doc)
                if word in doc.keys():
                    doc[word] += 1
                else:
                    doc[word] = 1

                if word in docs_summary__.keys():
                    docs_summary__[word] += 1
                else:
                    docs_summary__[word] = 1
            
            docs_summary.append(docs_summary__)
            # doc = {}
            docs_desc__ = {}
            for word in report.description['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
                if word in doc.keys():
                    doc[word] += 1
                else:
                    doc[word] = 1

                if word in docs_desc__.keys():
                    docs_desc__[word] += 1
                else:
                    docs_desc__[word] = 1
            # print(vocab)
            docs_desc.append(docs_desc__)
            docs.append(doc)

        for src in sources.values():
            d1 = {}
            for word in src.file_name['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
                if word in d1.keys():
                    d1[word] += 1
                else:
                    d1[word] = 1
            # print(vocab)
            docs_class_name.append(d1)

            d2 = {}
            for word in src.attributes['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
                if word in d2.keys():
                    d2[word] += 1
                else:
                    d2[word] = 1
            # print(vocab)
            docs_atr.append(d2)

            d3 = {}
            for word in src.method_names['unstemmed']:
                if word not in vocab:
                    vocab.append(word)

                if word in d3.keys():
                    d3[word] += 1
                else:
                    d3[word] = 1
            # print(vocab)
            docs_method.append(d3)

            d4 = {}
            for word in src.comments['unstemmed']:
                if word not in vocab:
                    vocab.append(word)
                if word in d4.keys():
                    d4[word] += 1
                else:
                    d4[word] = 1
            # print(vocab)
            docs_com.append(d4)
            # docs.append(doc)
            # docs.append(doc)

        x_tfidf = []
        for doc in docs_summary:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_summary)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            x_tfidf.append(row)

        y_tfidf = []
        for doc in docs_desc:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_desc)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            y_tfidf.append(row)

        s1 = []
        for doc in docs_class_name:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_class_name)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            s1.append(row)

        s2 = []
        for doc in docs_atr:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_atr)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            s2.append(row)

        s3 = []
        for doc in docs_method:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_method)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            s3.append(row)

        s4 = []
        for doc in docs_com:
            for word in doc:
                doc[word] = self.tfidf(word, doc, docs_com)
            row = []
            for f in vocab:
                if f in doc.keys():
                    row.append(doc[word])
                else:
                    row.append(0)
            s4.append(row)
        # should save sparse matrix
        return x_tfidf, y_tfidf, s1, s2, s3, s4

    def compute_similarity(self, x_tfidf, y_tfidf, s1, s2, s3, s4):
        """
        compute similarity
        """
        n = len(x_tfidf)
        m = len(s1)
        size = len(x_tfidf[n-1])
        x_tfidf = np.asarray(x_tfidf)
        y_tfidf = np.asarray(y_tfidf)
        s1 = np.asarray(s1)
        s2 = np.asarray(s2)
        s3 = np.asarray(s3)
        s4 = np.asarray(s4)
        x_similarity = np.empty((n, m), dtype=object)
        print(n)
        print(m)
        print(size)
        for i in range(n):
            for j in range(m):
                x_similarity[i][j] = (
                    cosine_similarity(x_tfidf[i].reshape(1, size), s1[j].reshape(1, size))[0][0]
                    + cosine_similarity(x_tfidf[i].reshape(1, size), s2[j].reshape(1, size))[0][0]
                    + cosine_similarity(x_tfidf[i].reshape(1, size), s3[j].reshape(1, size))[0][0]
                    + cosine_similarity(x_tfidf[i].reshape(1, size), s4[j].reshape(1, size))[0][0]
                    + cosine_similarity(y_tfidf[i].reshape(1, size), s1[j].reshape(1, size))[0][0]
                    + cosine_similarity(y_tfidf[i].reshape(1, size), s2[j].reshape(1, size))[0][0]
                    + cosine_similarity(y_tfidf[i].reshape(1, size), s3[j].reshape(1, size))[0][0]
                    + cosine_similarity(y_tfidf[i].reshape(1, size), s4[j].reshape(1, size))[0][0]
                )
        return x_similarity
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    tf = TFIDFVectorizer()
    x, y, s1, s2, s3, s4 = tf.compute_tfidf_summary(bug_reports, src_files)
    text_structure = tf.compute_similarity(x, y, s1, s2, s3, s4)
    print(text_structure)
    numpyData = {"data": text_structure}
    with open(DATASET.root / 'text_structure.json', 'w') as file:
        json.dump(numpyData, file, cls=NumpyArrayEncoder)


if __name__ == '__main__':
    main()
