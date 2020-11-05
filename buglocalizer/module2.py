import pickle
from datasets import DATASET
from math import log
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import gensim
import gensim.models
from datetime import datetime

model = "../data/glove.6B.100d.txt"

# print(word_vectors.most_similar("abc"))

import numpy as np

def testWiki():
    embeddings_index = {}
    with open('../data/glove.6B.100d.txt', encoding='utf8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            embed = np.array(values[1:], dtype=np.float32)
            embeddings_index[word] = embed
            # print(word)
    # print(embeddings_index[b"the"])
    print('Loaded %s word vectors.' % len(embeddings_index))
    # print(b'pink' in embeddings_index.keys())
    # # Embeddings for available words
    # data_embeddings = {key: value for key, value in embeddings_index.items() if key in categories.keys()}
    # # Processing the query
    # def process(query):
    #     query_embed = embeddings_index[query]
    #     # print(query_embed)
    #     scores = {}
    #     for word, embed in data_embeddings.items():
    #         category = categories[word]
    #         dist = query_embed.dot(embed)
    #         dist /= len(data[category])
    #         scores[category] = scores.get(category, 0) + dist
    #     return scores

    # # Testing
    # print(process(b'pink'))
    # print(process(b'frank'))
    # print(process(b'moscow'))
    return embeddings_index

def getVocab(src_files, bug_reports):
    embeddings_index = testWiki()
    all_glove_words = list(embeddings_index.keys())
    docs_report = []
    docs_source = []
    for report in bug_reports.values():
        data = report.pos_tagged_summary['stemmed'] +  report.pos_tagged_description['stemmed']
        docs_report.append(set(data))

    for src in src_files.values():
        data = src.class_names['stemmed'] + src.method_names['stemmed']
        docs_source.append(set(data))
    n = len(docs_report)
    m = len(docs_source)
    output = []
    print(datetime.now())

    # cần tiền xử lí: chỉ lấy những word thuộc all_glove_word trong bug, source
    # similar của 1 từ thuộc bug với 1 từ thuộc source 
    for i, bug in enumerate(docs_report):
        print(i)
        x = []
        for j, source in enumerate(docs_source):
            print(j)
            array_sum = []
            for word_report in bug:
                if(word_report in all_glove_words):
                    print(datetime.now())
                    array_max = []
                    embedding_word_report = embeddings_index[word_report].reshape(1, 100)
                    for word_source in source:
                        if word_source in all_glove_words:
                            array_max.append(cosine_similarity(embedding_word_report, embeddings_index[word_source].reshape(1, 100))[0][0])
                    if len(array_max) == 0:
                        array_sum.append(0)
                    else:
                        array_sum.append(max(array_max))
            x.append(1/ 2 * (sum(array_sum) / n))
            # print(sum(array_sum))
            # z = 1 / 2 * (sum([max([cosine_similarity(embeddings_index[word_report].reshape(1, 100), embeddings_index[word_source].reshape(1, 100))[0][0] for word_source in source if word_source in all_glove_words]) for word_report in bug if word_report in all_glove_words] ) / n)
            # print(z)
            print("End ", datetime.now())
        output.append(x)
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
    sim = getVocab(src_files, bug_reports)

    with open(DATASET.root / 'module2.json', 'w') as file:
        json.dump(sim, file)


if __name__ == '__main__':
    main()
