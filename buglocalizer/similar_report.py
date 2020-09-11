import pickle
import json
from collections import OrderedDict
from math import log
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
from datasets import DATASET
import datetime
import os.path
import numpy as np

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

            for word in report.description['unstemmed']:
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
    def compute_similarity(self, x_tfidf, y_tfidf):
        """
        compute similarity
        """
        n = len(x_tfidf)
        size = len(x_tfidf[n-1])
        x_tfidf = np.asarray(x_tfidf)
        x_similarity = np.empty((n, n), dtype=object) 
        for i in range(n):
            for j in range(n):     
                x_similarity[i][j] = cosine_similarity(x_tfidf[i].reshape(1,size), y_tfidf[j].reshape(1,size))[0][0]
        return x_similarity

def similar_report_scores(src_files, bug_reports):
    # duyệt từng bug
    tf = TFIDFVectorizer()
    x_tfidf = tf.compute_tfidf_summary(bug_reports)
    n = len(x_tfidf)
    size = len(x_tfidf[n-1])
    x_tfidf = np.asarray(x_tfidf)
    similarity_report_scores = []
    for r1, report in enumerate(bug_reports.values()):
        print(r1)
        scores = []
        input_bug_report = int(report.opendate)

        # x là tập B
        x = []
        for rep in bug_reports.values():
            fixed_date_bug = int(rep.fixdate)
            if (input_bug_report > fixed_date_bug):
                x.append(rep)
        # duyệt từng file
        for src in src_files.values():
            if(len(x) != 0):
                simi_score = 0

                # duyệt b trong B
                for i, relevant_commit in enumerate(x):
                    files = [r.split('.')[-2]
                             for r in relevant_commit.fixed_files]

                    # duyệt từng file f trong b để tìm đc file tương ứng
                    for f in files:
                        f = f.split('\\')[-1]
                        exact_file_name = src.exact_file_name.split(' ')[-1]
                        if(exact_file_name == f):
                            # print(relevant_commit.summary['unstemmed'])
                            # print(report.summary['unstemmed'])
                            # tc = (input_bug_report - datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()) / 60/60/24
                            # tc = (input_bug_report - int(relevant_commit.fixdate)) / 60 / 60 / 24
                            
                            simi_score += cosine_similarity(x_tfidf[r1].reshape(1,size), x_tfidf[i].reshape(1,size))[0][0]
                   
                scores.append(simi_score)
            else:
                scores.append(0)
        similarity_report_scores.append(scores)
    return similarity_report_scores


def main():
    # custom max rank = 10 and add set C
    with open('../preprocess_data/preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open('../preprocess_data/preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    scores = similar_report_scores(src_files, bug_reports)
    print(len(scores))
    print(len(scores[0]))
    with open(DATASET.root / 'similar_report.json', 'w') as file:
        json.dump(scores, file)


if __name__ == '__main__':
    main()
