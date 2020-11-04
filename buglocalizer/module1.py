import pickle
from datasets import DATASET
from math import log
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

def getModule1(src_files, bug_reports):
    # for report in bug_reports.values():
    #     print(report.id)
    for source in src_files.values():
        print(source.exact_file_name)
        print(source.class_names_hub)
        print(source.method_names_hub)
        print(source.variables_hub)
        print(source.attributes_hub)
        print("Commentssss", len(source.comments['stemmed']))
        print("Commentssss", len(source.pos_tagged_comments['stemmed']))
        break
def getVocab(src_files, bug_reports):
    vocab = []
    docs_report = []
    docs_source = []
    for report in bug_reports.values():
        docs_report__ = {}
        data = report.pos_tagged_summary['stemmed'] +  report.pos_tagged_description['stemmed']
        for word in data:
            if word not in vocab:
                vocab.append(word)

            if word in docs_report__.keys():
                docs_report__[word] += 1
            else:
                docs_report__[word] = 1
        
        docs_report.append(docs_report__)

    for src in src_files.values():
        docs_source_ = {}
        data = src.class_names['stemmed'] + src.method_names['stemmed']
        for word in data:
            if word not in vocab:
                vocab.append(word)
            if word in docs_source_.keys():
                docs_source_[word] += 1
            else:
                docs_source_[word] = 1
        docs_source.append(docs_source_)
        
    print(len(vocab))

    report_idf = []
    for doc in docs_report:
        for word in doc:
            doc[word] = idf(word, docs_report)
        row = []
        for f in vocab:
            if f in doc.keys():
                row.append(doc[word])
            else:
                row.append(0)
        report_idf.append(row)
    print("report_idf")

    source_idf = []
    for doc in docs_source:
        for word in doc:
            doc[word] = idf(word, docs_source)
        row = []
        for f in vocab:
            if f in doc.keys():
                row.append(doc[word])
            else:
                row.append(0)
        source_idf.append(row)
    print("source_idf")
    size = len(vocab)
    n = len(report_idf)
    m = len(source_idf)
    report_idf = np.asarray(report_idf)
    source_idf = np.asarray(source_idf)
    output = []

    for i in range(n):
        print(i)
        array_i = []
        __x = report_idf[i].reshape(1, size)
        for j in range(m):
            # t = max(cosine_similarity(__x, y_tfidf[j].reshape(1, size))[0][0], cosine_similarity(__x, s3[j].reshape(1, size))[0][0])
            t = cosine_similarity(__x, source_idf[j].reshape(1, size))[0][0]
            array_i.append(t)
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
    sim = getVocab(src_files, bug_reports)

    with open(DATASET.root / 'module1.json', 'w') as file:
        json.dump(sim, file)


if __name__ == '__main__':
    main()