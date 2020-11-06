import pickle
from datasets import DATASET
from math import log
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import gensim
import gensim.models
from datetime import datetime
from json import JSONEncoder

import numpy as np

def testWiki():
    embeddings_index = {}
    with open('../data/glove.6B.100d.txt', encoding='utf8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            embed = np.array(values[1:], dtype=np.float32)
            embeddings_index[word] = embed
    print('Loaded %s word vectors.' % len(embeddings_index))
    return embeddings_index

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def getVocab(src_files, bug_reports):
    now = datetime.now()
    embeddings_index = testWiki()
    all_glove_words = list(embeddings_index.keys())
    docs_report = []
    docs_source = []
    for report in bug_reports.values():
        data = report.pos_tagged_summary['stemmed'] +  report.pos_tagged_description['stemmed']
        array = set(data)
        out = []
        for element in array:
            if element in all_glove_words:
                out.append(embeddings_index[element])
        docs_report.append(out)

    for src in src_files.values():
        data = src.class_names['stemmed'] + src.method_names['stemmed']
        array = set(data)
        out = []
        for element in array:
            if element in all_glove_words:
                out.append(embeddings_index[element])
        docs_source.append(out)
    data_report = {"data": docs_report}
    data_source = {"data": docs_source}
    with open(DATASET.root / 'semantic_report.json', 'w') as file:
        json.dump(data_report, file, cls=NumpyArrayEncoder)
    with open(DATASET.root / 'semantic_source.json', 'w') as file:
        json.dump(data_source, file, cls=NumpyArrayEncoder)
    print(datetime.now() - now)

def matrix_sim(R, S):
    d_matrix = np.dot(R, S.T)

    squared_R = np.sqrt(np.sum(R**2, axis=1)).reshape(-1, 1)
    squared_S = np.sqrt(np.sum(S**2, axis=1)).reshape(-1, 1)

    norm = np.dot(squared_R, squared_S.T)

    return np.multiply(d_matrix, 1/norm)
def result():
    with open(DATASET.root / 'semantic_report.json', 'rb') as file:
        bug_reports= json.load(file)["data"]
    with open(DATASET.root / 'semantic_source.json', 'rb') as file:
        src_files = json.load(file)["data"]
    output = []
    print(len(bug_reports))
    for i, bug in enumerate(bug_reports):
        print(i)
        array_i = []
        if(len(bug) == 0):
            for source in src_files:
                array_i.append(0)
            output.append(array_i)
            continue
        x = np.array(bug)
        for source in src_files:
            if len(source) == 0:
                array_i.append(0)
                continue
            y = np.array(source)
            array_i.append(1 / 2 * (sum([max([w_ for w_ in w]) for w in matrix_sim(x, y)]) / len(x) + sum([max([w_ for w_ in w]) for w in matrix_sim(y, x)]) / len(y)))
        output.append(array_i)
    return output

def idf(word,doc_list):
    all_num=len(doc_list)
    word_count=0
    for doc in doc_list:
        if word in doc:
            word_count+=1
    return log((all_num + 1)/(word_count))

def main():
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    # getModule1(src_files, bug_reports)
    # sim = getVocab(src_files, bug_reports)
    sim = result()

    with open(DATASET.root / 'module2.json', 'w') as file:
        json.dump(sim, file)


if __name__ == '__main__':
    main()
