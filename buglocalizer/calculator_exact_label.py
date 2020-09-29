
import pickle
import json
import numpy as np
from datasets import DATASET

def label(label, extract_features):
    results = []
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    f5 = 0
    for i, bug in enumerate(label):
        b = []
        for source_id in bug:
            b.append(extract_features[i][source_id])
            
            if(extract_features[i][source_id][0] > 0.5):
                # print(i, source_id)
                f1 = f1 + 1
            if(extract_features[i][source_id][1] > 0.5):
                # print(i, source_id)
                f2 = f2 + 1
            if(extract_features[i][source_id][2] > 0.5):
                # print(i, source_id)
                f3 = f3 + 1
            if(extract_features[i][source_id][3] > 0.5):
                # print(i, source_id)
                f4 = f4 + 1
            if(extract_features[i][source_id][4] > 0.5):
                # print(i, source_id)
                f5 = f5 + 1
        results.append(b)
    # print(len(src_files))
    print(f1)
    print(f2)
    print(f3)
    print(f4)
    print(f5)
    return results

def main():

    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label_1 = json.load(file)
    with open(DATASET.root / 'extract_features.json', 'rb') as file:
        extract_features = json.load(file)
    results = label(label_1, extract_features)
    # print(len(src_files))
    # print(len(bug_reports))
    # with open(DATASET.root / 'data_label_1.json', 'w') as file:
    #     json.dump(results, file)
    # with open(DATASET.root / 'source_tfidf.json', 'w') as file:
    #     json.dump(y, file)



if __name__ == '__main__':
    main()
