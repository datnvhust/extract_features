import pickle
import json
from collections import OrderedDict

from datasets import DATASET
import datetime
import os.path
import numpy as np


def similar_report_scores(src_files, bug_reports):
    # duyệt từng bug
    similarity_report_scores = []
    for report in bug_reports.values():
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
                            print(relevant_commit.summary['unstemmed'])
                            print(report.summary['unstemmed'])
                            # tc = (input_bug_report - datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()) / 60/60/24
                            # tc = (input_bug_report - int(relevant_commit.fixdate)) / 60 / 60 / 24
                            
                            # simi_score += 1 / ( 1 + np.exp(tc / k))
                   
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
