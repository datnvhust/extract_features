import json
from datasets import DATASET
import numpy as np

def main():
    with open(DATASET.root / 'ranking.json', 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    for i, bug in enumerate(label):
        x = []
        for source in bug:
            if(ranking[i].index(source) == 0):
                print(i, source)
                count = count + 1
            x.append(ranking[i].index(source))
        out.append(x)
    print(count)
    with open(DATASET.root / 'ranking_label.json', 'w') as file:
        json.dump(out, file)

def main_normal():
    with open(DATASET.root / 'ranking_normal.json', 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    for i, bug in enumerate(label):
        x = []
        for source in bug:
            if(ranking[i].index(source) == 0):
                print(i, source)
                count = count + 1
            x.append(ranking[i].index(source))
        out.append(x)
    print(count) # 43/535 no tests , 71/587 all
    with open(DATASET.root / 'ranking_label_normal.json', 'w') as file:
        json.dump(out, file)


if __name__ == '__main__':
    # main()
    main_normal()
