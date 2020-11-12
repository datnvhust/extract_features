
import pickle
import json
import numpy as np
from datasets import DATASET

def label(bug_reports, src_files):
    results = []
    for i, bug in enumerate(bug_reports.values()):
        b = []
        for files in bug.fixed_files:
            array_split = files.split('\\')
            # array_split[-1] = bug.commit + " " + array_split[-1]
            exact_file_name = "/".join(array_split)
            if exact_file_name in src_files:
                b.append(src_files.index(exact_file_name))
        results.append(b)
    # print(len(src_files))
    return results

def label_v2(bug_reports, src_files):
    results = []
    for i, bug in enumerate(bug_reports.values()):
        b = []
        x = []
        fixed_files = []
        for files in bug.fixed_files:
            array_split = files.split('\\')
            exact_file_name = "/".join(array_split)
            fixed_files.append(exact_file_name)
        for src in src_files:
            if(src in fixed_files):
                x.append(1)
            else:
                x.append(0)
            # if exact_file_name in src_files:
            #     b.append(src_files.index(exact_file_name))
        results.append(x)
    return results

def main():

    with open(DATASET.root / 'preprocessed_src_id.json', 'rb') as file:
        src_files = json.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    src_process = []
    for src in src_files:
        src_split = src.split("/")
        src_split[-1] = src_split[-1].split(" ")[-1]
        src_process.append('/'.join(src_split))
        # print(src)
        # print("/".join(src_split))
    print(src_process[23])
    for bug in bug_reports.values():
        print(bug.commit)
        break
    results = label(bug_reports, src_process)
    # print(len(src_files))
    # print(len(bug_reports))
    with open(DATASET.root / 'name_src_label_1.json', 'w') as file:
        json.dump(results, file)
    # with open(DATASET.root / 'source_tfidf.json', 'w') as file:
    #     json.dump(y, file)

def main_v2():

    with open(DATASET.root / 'preprocessed_src_id.json', 'rb') as file:
        src_files = json.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    
    src_process = []
    for src in src_files:
        src_split = src.split("/")
        src_split[-1] = src_split[-1].split(" ")[-1]
        src_process.append('/'.join(src_split))

    results = label_v2(bug_reports, src_process)
    with open(DATASET.root / 'label.json', 'w') as file:
        json.dump(results, file)
def load():
    main()
    main_v2()
if __name__ == '__main__':
    main()
    main_v2()
