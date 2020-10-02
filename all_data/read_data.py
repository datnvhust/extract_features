
import pickle
import json
from math import log
import numpy as np
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
            docs_source.append(docs_source_)
            # print(src.id)
            # print(src.method_names_hub)
            # src.method_names_hub = self._split_camelcase(src.method_names_hub)
            # methodnames_punctnum_rem = [token.translate(punctnum_table)
            #                             for token in src.method_names_hub]
            # src.method_names_hub = [token.lower() for token
            #                     in methodnames_punctnum_rem if token]
            # src.method_names_hub = [token for token in src.method_names_hub
            #                     if token not in stop_words]
            # src.method_names_hub = [token for token in src.method_names_hub
            #                     if token not in java_keywords]
            # print(src.method_names_hub)
            d3 = {}
            # for method in src.method_names_hub:
            #     src.method_names_hub = self._split_camelcase(src.method_names_hub)
            #     methodnames_punctnum_rem = [token.translate(punctnum_table)
            #                                 for token in src.method_names_hub]
            #     src.method_names_hub = [token.lower() for token
            #                         in methodnames_punctnum_rem if token]
            #     src.method_names_hub = [token for token in src.method_names_hub
            #                         if token not in stop_words]
            #     src.method_names_hub = [token for token in src.method_names_hub
            #                         if token not in java_keywords]
            for word in src.method_names_hub:
                # if word not in vocab:
                #     vocab.append(word)

                if word in d3.keys():
                    d3[word] += 1
                else:
                    d3[word] = 1
            # print(vocab)
            docs_method.append(d3)

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

        return x_tfidf, y_tfidf, s3
    
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
    print(len(src_files))
    tf = TFIDFVectorizer()
    x, y, s3 = tf.compute_tfidf_summary(bug_reports, src_files)
    print(len(x))
    print(len(y))
    with open(DATASET.root / 'x_tfidf.json', 'w') as file:
        json.dump(x, file)
    with open(DATASET.root / 'y_tfidf.json', 'w') as file:
        json.dump(y, file)

    with open(DATASET.root / 's3.json', 'w') as file:
        json.dump(s3, file)
    with open(DATASET.root / 'features1_update.json', 'rb') as file:
        z = json.load(file)['data']
    print(len(z))


    # with open(DATASET.root / 'x_tfidf.json', 'rb') as file:
    #     x = json.load(file)
    # with open(DATASET.root / 'y_tfidf.json', 'rb') as file:
    #     y = json.load(file)
    # with open(DATASET.root / 's3.json', 'rb') as file:
    #     s3 = json.load(file)
    # tf = TFIDFVectorizer()
    text_structure = tf.compute_similarity(x, y, s3)
    print(text_structure)

    output = []
    min_score = np.min(text_structure)
    max_score = np.max(text_structure)
    max_min = max_score - min_score
    for bug in text_structure:
        scores = []
        for source in bug:
            scores.append((source - min_score) / max_min)
        output.append(scores)
    # print(output)
    numpyData = {"data": output}
    with open(DATASET.root / 'features1_update.json', 'w') as file:
        json.dump(numpyData, file, cls=NumpyArrayEncoder)
    



if __name__ == '__main__':
    main()
