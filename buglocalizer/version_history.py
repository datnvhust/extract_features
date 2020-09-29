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
    k = 45
    for report in bug_reports.values():
        print(report.commit)
        # tìm các commit trong vòng 15 ngày (sẽ chứa các file)
        scores = []
        # input_bug_report = datetime.datetime.strptime(
            # report.opendate, '%Y-%m-%d %H:%M:%S').timestamp()
        input_bug_report = int(report.opendate)
        # print(input_bug_report)
        x = []
        for rep in bug_reports.values():
            # commit_date = datetime.datetime.strptime(
            #     rep.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()
            commit_date = int(rep.fixdate)
            if (input_bug_report > commit_date) and (input_bug_report - commit_date < 1 * 60 * 60 * 24 * k):
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
                        f = f.split('\\')[-1]
                        exact_file_name = src.exact_file_name.split(' ')[-1]
                        # print(exact_file_name, f)
                        # if(src.exact_file_name == f):
                        if(exact_file_name == f):
                            # k = 15
                            # tc = (input_bug_report - datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp()) / 60/60/24
                            tc = (input_bug_report - int(relevant_commit.fixdate)) / 60 / 60 / 24
                            # print(datetime.datetime.strptime(
                            #     relevant_commit.fixdate, '%Y-%m-%d %H:%M:%S').timestamp())
                            history_score += 1 / ( 1 + np.exp(tc / k))
                # Nếu file không thuộc các commit trên thì bỏ
                scores.append(history_score)
            else:
                scores.append(0)
        version_history_scores.append(scores)
        # all_simis.append(scores)
    return version_history_scores


def main():
    # custom max rank = 10 and add set C
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    version_history_scores = version_history(src_files, bug_reports)
    print(len(version_history_scores))
    print(len(version_history_scores[0]))
    max_score = np.max(version_history_scores)
    # print(np.min(version_history_scores))
    count_0 = 0
    output = []
    for bug in version_history_scores:
        scores = []
        for source in bug:
            if source == 0:
                count_0 = count_0 + 1
            scores.append( source / max_score)
        output.append(scores)
    # print(output)
    print(count_0)

    with open(DATASET.root / 'version_history.json', 'w') as file:
        json.dump(output, file)


if __name__ == '__main__':
    main()

    # tăng k

# k = 30: 511068
# k = 15: 524200
# k = 45: 499767