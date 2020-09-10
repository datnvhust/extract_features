import pickle
import json
from collections import OrderedDict

from datasets import DATASET
import datetime
import os.path
import numpy as np


def version_history(src_files, bug_reports):
    # duyệt từng bug
    version_history_scores = []
    for report in bug_reports.values():
        # print(report.opendate)
        # summary = nlp(' '.join(report.summary['unstemmed']))
        # print(summary)
        # summary = tfidf.fit_transform(report.summary['unstemmed'])
        # print(summary)
        # description = nlp(' '.join(report.description['unstemmed']))
        # print(report.pos_tagged_summary['unstemmed'])
        # print(summary.similarity(description))

        # tìm các commit trong vòng 15 ngày (sẽ chứa các file)
        scores = []
        input_bug_report = datetime.datetime.strptime(
            report.opendate, '%Y-%m-%d %H:%M:%S').timestamp()
        x = []
        for rep in bug_reports.values():
            commit_date = datetime.datetime.strptime(
                rep.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()
            if (input_bug_report > commit_date) and (input_bug_report - commit_date < 1 * 60 * 60 * 24 * 15):
                # print((input_bug_report - commit_date)/1 / 60 / 60 / 24)
                # x = [r.split('.')[-2]
                #      for r in rep.fixed_files]
                # print(x)
                # rep.fixed_files = [r.split('.')[-2]
                #              for r in rep.fixed_files]
                x.append(rep)

        # duyệt từng file
        for src in src_files.values():
            if(len(x) != 0):
                # files = [r.split('.')[-2]
                #          for r in rep.fixed_files]
                # duyệt từng commit c trong relevant, kiểm tra có file f trong đó k
                # x = 0
                history_score = 0
                for i, relevant_commit in enumerate(x):
                    files = [r.split('.')[-2]
                             for r in relevant_commit.fixed_files]
                    for f in files:
                        # print(src.exact_file_name, f)
                        if(src.exact_file_name == f):
                            k = 15
                            tc = (input_bug_report - datetime.datetime.strptime(
                                relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()) / 60/60/24
                            # print(f)
                            # print(datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp())
                            # print(input_bug_report)
                            # print((input_bug_report - datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()) / 60/60/24)
                            history_score += 1 / ( 1 + np.exp(tc / k))
                    # print(src.exact_file_name, relevant_commit)
                # if(src.exact_file_name in x):
                #     print(src.exact_file_name)
                # print(src.exact_file_name)
                # Nếu file không thuộc các commit trên thì bỏ
                scores.append(history_score)
            else:
                scores.append(0)
        version_history_scores.append(scores)
        # all_simis.append(scores)
    print(version_history_scores)


def main():
    # custom max rank = 10 and add set C
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    version_history(src_files, bug_reports)

    # with open(DATASET.root / 'stack_trace.json', 'w') as file:
    #     json.dump(all_scores, file)


if __name__ == '__main__':
    main()
