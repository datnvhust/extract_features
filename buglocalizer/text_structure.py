import en_vectors_web_lg

import pickle
import json

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from datasets import DATASET


def calculate_similarity(src_files, bug_reports):
    
    # Loading word vectors
    nlp = en_vectors_web_lg.load()
    # src_docs = [nlp(' '.join(src.file_name['unstemmed'] + src.class_names['unstemmed']
    #                          + src.attributes['unstemmed'] + src.comments['unstemmed']
    #                          + src.method_names['unstemmed']))
    #             for src in src_files.values()]
    # # print(src_docs[0])
    # # src_docs là mảng chứa tất cả files, 1 phần tử đại diện cho 1 file được gộp bởi file_name, class_name,...
    # min_max_scaler = MinMaxScaler()
    
    all_simis = []
    
    for report in bug_reports.values():
        # report_doc = nlp(' '.join(report.summary['unstemmed']
        #                           + report.pos_tagged_description['unstemmed']))
        scores = []
        # print(report.summary['unstemmed'])
        summary = nlp(' '.join(report.summary['unstemmed']))
        # print(summary)
        description = nlp(' '.join(report.description['unstemmed']))
        # print(report.pos_tagged_summary['unstemmed'])
        # print(summary.similarity(description))
        for src in src_files.values():
            class_names = nlp(' '.join(src.class_names['unstemmed']))
            attributes = nlp(' '.join(src.attributes['unstemmed']))
            comments = nlp(' '.join(src.comments['unstemmed']))
            method_names = nlp(' '.join(src.method_names['unstemmed']))

            simi = (summary.similarity(class_names)
                    + summary.similarity(attributes)
                    + summary.similarity(comments)
                    + summary.similarity(method_names)
                    + description.similarity(class_names)
                    + description.similarity(attributes)
                    + description.similarity(comments)
                    + description.similarity(method_names))
            scores.append(simi)
        
        all_simis.append(scores)
        # print(scores)
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
