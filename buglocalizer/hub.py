import en_vectors_web_lg

import pickle
import json

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from datasets import DATASET

import networkx as nx 


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

def hub(src_files, bug_reports):
    results = []
    for s1, src1 in enumerate(src_files.values(), 1):
        # class_names = nlp(' '.join(src.class_names['unstemmed']))
        # attributes = nlp(' '.join(src.attributes['unstemmed']))
        # comments = nlp(' '.join(src.comments['unstemmed']))
        # method_names = nlp(' '.join(src.method_names['unstemmed']))

        # print("abc", src.class_names_1)
        # print(s)

        cont = False
        for c in src1.class_names_1:
            if cont == True:
                break
            for s2, src2 in enumerate(src_files.values(), 1):
                if s1 == s2:
                    break
                if search(src2.class_names_1, c) == True:
                    results.append((s1, s2))
                    cont == True
                    break
        
    print(results)
    G = nx.DiGraph() 
    G.add_edges_from(results)
    nx.draw_networkx(G, with_labels = True) 
    hubs, authorities = nx.hits(G, max_iter = 50, normalized = True) 
    # The in-built hits function returns two dictionaries keyed by nodes 
    # containing hub scores and authority scores respectively. 
    
    print("Hub Scores: ", hubs) 
    print("Authority Scores: ", authorities) 
    return hubs



def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    hubs = hub(src_files, bug_reports)

    with open(DATASET.root / 'hub.json', 'w') as file:
        json.dump(hubs, file)


if __name__ == '__main__':
    main()
