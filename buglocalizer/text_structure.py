# import en_vectors_web_lg

import pickle
import json

import numpy as np
from sklearn.preprocessing import MinMaxScaler
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import DATASET
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
    
def main():
    
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
        
    all_simis = calculate_similarity(src_files, bug_reports)

    with open(DATASET.root / 'text_structure.json', 'w') as file:
        json.dump(all_simis, file)


if __name__ == '__main__':
    main()
