import pickle
import json

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import DATASET
from datetime import datetime
import networkx as nx


def searchList(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


def search(x, platform):
    if x == platform:
        return True
    return False


def hub(src_files, bug_reports):
    results = []
    for s1, src1 in enumerate(src_files.values(), 1):
        # class_names = nlp(' '.join(src.class_names['unstemmed']))
        # attributes = nlp(' '.join(src.attributes['unstemmed']))
        # comments = nlp(' '.join(src.comments['unstemmed']))
        # method_names = nlp(' '.join(src.method_names['unstemmed']))

        # print(src1.exact_file_name.split(' ')[-1])
        # print(src1.class_names_hub)
        # print(src1.method_names)
        # print(src1.method_names_hub)
        # print(src1.variables_hub)
        # print(src1.class_imports)
        print(src1.exact_file_name)
        # print(src1.class_imports)
        # print(src1.attributes)
        # print(s)/
        src1_name = src1.exact_file_name.split(' ')[-1]
        cont = False

        for s2, src2 in enumerate(src_files.values(), 1):
            if s1 == s2:
                break
            
            for class_import in src2.class_imports:
                if class_import == src1_name:
                    results.append((s1, s2))
                    break
            # for c in src1.class_names_hub:
            #     if cont == True:
            #         break
            # print(src2.exact_file_name.split(' ')[-1], src1.exact_file_name.split(' ')[-1])
            # if search(src2.exact_file_name.split(' ')[-1], src1.exact_file_name.split(' ')[-1]) == True:
            #     print(src2.exact_file_name.split(' ')[-1])
            #     print(src2.method_names_hub)
            #     print(src1.method_names_hub)
            #     print(src1.variables_hub)
            #     results.append((s1, s2))
            #     cont == True
            #     break

        # inner class
        # for s2, src2 in enumerate(src_files.values(), 1):
        #     if s1 == s2:
        #         break
        #     # for c in src1.class_names_hub:
        #     #     if cont == True:
        #     #         break
        #     # print(src2.exact_file_name.split(' ')[-1], src1.exact_file_name.split(' ')[-1])
        #     # if search(src2.exact_file_name.split(' ')[-1], src1.exact_file_name.split(' ')[-1]) == True:
        #     #     print(src2.exact_file_name.split(' ')[-1])
        #     #     print(src2.method_names_hub)
        #     #     print(src1.method_names_hub)
        #     #     print(src1.variables_hub)
        #     #     results.append((s1, s2))
        #     #     cont == True
        #     #     break

        #     for method in src1.method_names_hub:
        #         if cont == True:
        #             break
        #         if searchList(src2.method_names_hub, method):
        #             results.append((s1, s2))
        #             cont == True
        #             break
            
        #     for method in src1.attributes_hub:
        #         if cont == True:
        #             break
        #         if searchList(src2.attributes_hub, method):
        #             results.append((s1, s2))
        #             cont == True
        #             break

    print(results)
    G = nx.DiGraph()
    G.add_edges_from(results)
    nx.draw_networkx(G, with_labels=True)
    hubs, authorities = nx.hits(G, max_iter=5000 * 5000, normalized=True)
    # The in-built hits function returns two dictionaries keyed by nodes
    # containing hub scores and authority scores respectively.

    # print("Hub Scores: ", hubs)
    # print("Authority Scores: ", authorities)
    return hubs


def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    s1 = datetime.now()
    print(s1)
    hubs = hub(src_files, bug_reports)
    # print(len(hub))
    s2 = datetime.now()
    print(s2)
    with open(DATASET.root / 'hub.json', 'w') as file:
        json.dump(hubs, file)


if __name__ == '__main__':
    main()
