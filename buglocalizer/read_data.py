
import pickle
import json, csv
from math import log
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
from datasets import DATASET
from json import JSONEncoder
from assets import stop_words, java_keywords
import re
import string
import inflection

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

    def _split_camelcase(self, tokens):
    
        # Copy tokens
        # returning_tokens = tokens[:]
        returning_tokens = []
        
        for token in tokens:
            split_tokens = re.split(fr'[{string.punctuation}]+', token)
            # If token is split into some other tokens
            if len(split_tokens) > 1:
                # returning_tokens.remove(token)
                # Camel case detection for new tokens
                for st in split_tokens:
                    camel_split = inflection.underscore(st).split('_')
                    # if len(camel_split) > 1:
                    returning_tokens.append(st)
                    returning_tokens += camel_split
                    # else:
                    #     returning_tokens.append(st)
            else:
                camel_split = inflection.underscore(token).split('_')
                # if len(camel_split) > 1:
                # returning_tokens.append(st)
                returning_tokens += camel_split
    
        return returning_tokens

    def compute_tfidf_summary(self, bug_reports, sources, bug_commits):
        
        # print(len(bug_commits))
        # print(len(bug_commits[6]))
        # print(len(sources))
        # for rep in process_clean['summary']:
        #     print(rep)
        output = []
        output_tfidf = []
        for i, report in enumerate(bug_reports.values()):
            # if i == 5:
            print(i)
            vocab = []
            docs_report = []
            docs_source = []
            docs_method = []
            data = report.summary['stemmed'] +  report.description['stemmed']
            docs_report__ = {}
            for word in data:
                if word not in vocab:
                    vocab.append(word)

                if word in docs_report__.keys():
                    docs_report__[word] += 1
                else:
                    docs_report__[word] = 1
            
            docs_report.append(docs_report__)
            
            for j, bug_commit in enumerate(bug_commits[i]):
                path = bug_commit[0].replace('/', '\\')
                src = sources[path]
                # if j == 0:
                #     print(src.method_names_hub)
                #     print(src.method_names)
                # docs_source_ = {}
                data = src.file_name['stemmed']  + src.attributes['stemmed'] +  src.method_names['stemmed'] + src.comments['stemmed']
                for word in data:
                    if word not in vocab:
                        vocab.append(word)
                    # if word in docs_source_.keys():
                    #     docs_source_[word] += 1
                    # else:
                    #     docs_source_[word] = 1
                docs_source.append(src.all_content)
                # d3 = {}
                # for word in src.method_names_hub:
                #     if word in d3.keys():
                #         d3[word] += 1
                #     else:
                #         d3[word] = 1
                # docs_method.append(src.id)
            print(len(docs_source)) # 940
            print(len(vocab)) # 3410
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
            print("x_tfidf", len(x_tfidf))
            y_tfidf = []
            for doc in docs_source:
                # print(doc)
                for word in doc:
                    doc[word] = self.tfidf(word, doc, docs_source)
                # print(doc)
                row = []
                for f in vocab:
                    if f in doc.keys():
                        row.append(doc[word])
                    else:
                        row.append(0)
                y_tfidf.append(row)
            print("y_tfidf", len(y_tfidf))
            # s3 = []
            # for doc in docs_method:
            #     for word in doc:
            #         doc[word] = self.tfidf(word, doc, docs_method)
            #     row = []
            #     for f in vocab:
            #         if f in doc.keys():
            #             row.append(doc[word])
            #         else:
            #             row.append(0)
            #     s3.append(row)
            
            data = self.cosine_sim(x_tfidf, y_tfidf)
            output.append(data)
            output_tfidf.append([x_tfidf, y_tfidf])
                # name ='x_tfidf_' + str(i) + '.json'
                # with open(DATASET.root / name, 'w') as file:
                #     json.dump([x_tfidf, y_tfidf], file)
        return output_tfidf, output
        # print((sources['ajbrowser\\src\\org\\aspectj\\tools\\ajbrowser\\85a827a BrowserProperties.java'].id))
        # for i, src in enumerate(sources.values()):
        #     if i ==0:
        #         print(src)
        #         # print(src.exact_file_name)
        #         # print(src.package_name)
        #         # print(src.id.replace('\\', '/'))
        # for report in bug_reports.values():
        #     docs_report__ = {}
        #     data = report.summary['unstemmed'] +  report.description['unstemmed']
        #     for word in data:
        #         if word not in vocab:
        #             vocab.append(word)

        #         if word in docs_report__.keys():
        #             docs_report__[word] += 1
        #         else:
        #             docs_report__[word] = 1
            
        #     docs_report.append(docs_report__)

        # for src in sources.values():
        #     docs_source_ = {}
        #     data = src.file_name['unstemmed']  + src.attributes['unstemmed'] +  src.method_names['unstemmed'] + src.comments['unstemmed']
        #     for word in data:
        #         if word not in vocab:
        #             vocab.append(word)
        #         if word in docs_source_.keys():
        #             docs_source_[word] += 1
        #         else:
        #             docs_source_[word] = 1
        #     docs_source.append(docs_source_)
        #     d3 = {}
        #     for word in src.method_names_hub:
        #         # if word not in vocab:
        #         #     vocab.append(word)

        #         if word in d3.keys():
        #             d3[word] += 1
        #         else:
        #             d3[word] = 1
        #     # print(vocab)
        #     docs_method.append(d3)

        # x_tfidf = []
        # for doc in docs_report:
        #     for word in doc:
        #         doc[word] = self.tfidf(word, doc, docs_report)
        #     row = []
        #     for f in vocab:
        #         if f in doc.keys():
        #             row.append(doc[word])
        #         else:
        #             row.append(0)
        #     x_tfidf.append(row)
        # print("x_tfidf")
        # y_tfidf = []
        # for doc in docs_source:
        #     for word in doc:
        #         doc[word] = self.tfidf(word, doc, docs_source)
        #     row = []
        #     for f in vocab:
        #         if f in doc.keys():
        #             row.append(doc[word])
        #         else:
        #             row.append(0)
        #     y_tfidf.append(row)
        # print("y_tfidf")

        # s3 = []
        # for doc in docs_method:
        #     for word in doc:
        #         doc[word] = self.tfidf(word, doc, docs_method)
        #     row = []
        #     for f in vocab:
        #         if f in doc.keys():
        #             row.append(doc[word])
        #         else:
        #             row.append(0)
        #     s3.append(row)

        # return x_tfidf, y_tfidf, s3
    
    def cosine_sim(self, x_tfidf, y_tfidf):
        n = len(x_tfidf)
        m = len(y_tfidf)
        size = len(x_tfidf[n-1])
        # s3 = np.asarray(s3)
        x_tfidf = np.asarray(x_tfidf)
        y_tfidf = np.asarray(y_tfidf)
        x_similarity = []
        for i in range(n):
            print(i)
            array_i = []
            __x = x_tfidf[i].reshape(1, size)
            for j in range(m):
                # t = max(cosine_similarity(__x, y_tfidf[j].reshape(1, size))[0][0], cosine_similarity(__x, s3[j].reshape(1, size))[0][0])
                t = cosine_similarity(__x, y_tfidf[j].reshape(1, size))[0][0]
                array_i.append(t)
            x_similarity.append(array_i)
        return x_similarity
    
    def compute_similarity(self, x_tfidf, y_tfidf, s3):
        """
        compute similarity
        """
        n = len(x_tfidf)
        m = len(y_tfidf)
        size = len(x_tfidf[n-1])
        print(size)
        s3 = np.asarray(s3)
        x_tfidf = np.asarray(x_tfidf)
        y_tfidf = np.asarray(y_tfidf)
        x_similarity = np.empty((n, m), dtype=object)
        for i in range(n):
            print(i)
            __x = x_tfidf[i].reshape(1, size)
            for j in range(m):
                t = max(cosine_similarity(__x, y_tfidf[j].reshape(1, size))[0][0], cosine_similarity(__x, s3[j].reshape(1, size))[0][0])
                x_similarity[i][j] = t
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

    with open(DATASET.root / 'bug_commit.json', 'rb') as file:
        bug_commits = json.load(file)
    print(len(bug_reports))
    # print(x)
    for src in src_files.values():
        docs_source_ = {}
        data = src.file_name['stemmed']  + src.attributes['stemmed'] +  src.method_names['stemmed'] + src.comments['stemmed']
        for word in data:
            if word in docs_source_.keys():
                docs_source_[word] += 1
            else:
                docs_source_[word] = 1
        d3 = {}
        for word in src.method_names_hub:
            if word in d3.keys():
                d3[word] += 1
            else:
                d3[word] = 1
        src.all_content = docs_source_
        src.id = d3
    tf = TFIDFVectorizer()
    xy, output =  tf.compute_tfidf_summary(bug_reports, src_files, bug_commits)
    with open(DATASET.root / 'tfidf_test.json', 'w') as file:
        json.dump(xy, file)
    
    with open(DATASET.root / 'features1_update_v2.json', 'w') as file:
        json.dump(output, file)

    # with open(DATASET.root / 's3.json', 'w') as file:
    #     json.dump(s3, file)
    # with open(DATASET.root / 'features1_update.json', 'rb') as file:
    #     z = json.load(file)['data']
    # print(len(z))


    # # with open(DATASET.root / 'x_tfidf.json', 'rb') as file:
    # #     x = json.load(file)
    # # with open(DATASET.root / 'y_tfidf.json', 'rb') as file:
    # #     y = json.load(file)
    # # with open(DATASET.root / 's3.json', 'rb') as file:
    # #     s3 = json.load(file)
    # # tf = TFIDFVectorizer()
    # text_structure = tf.compute_similarity(x, y, s3)
    # print(text_structure)

    # output = []
    # min_score = np.min(text_structure)
    # max_score = np.max(text_structure)
    # max_min = max_score - min_score
    # for bug in text_structure:
    #     scores = []
    #     for source in bug:
    #         scores.append((source - min_score) / max_min)
    #     output.append(scores)
    # # print(output)
    # numpyData = {"data": output}
    # with open(DATASET.root / 'features1_update.json', 'w') as file:
    #     json.dump(numpyData, file, cls=NumpyArrayEncoder)
    



if __name__ == '__main__':
    main()
