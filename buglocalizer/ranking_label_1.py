import json
from datasets import DATASET
import numpy as np

def main(alpha):
    file_ = 'ranking_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    top5 = 0
    top10 = 0
    top20 = 0
    MRR = 0
    for i, bug in enumerate(label):
        x = []
        min = 10000000
        for source in bug:
            if(ranking[i].index(source) < 1):
                count = count + 1
            if min > ranking[i].index(source):
                min = ranking[i].index(source)
            x.append(ranking[i].index(source))
        if(min < 5):
            top5 = top5 + 1
        if(min < 10):
            top10 = top10 + 1
        if(min < 20):
            top20 = top20 + 1
        MRR = MRR + 1 / (min + 1)
        out.append(x)
    MRR = MRR / len(label)
    print(alpha, 'normal')
    print(count) 
    # 63/587 AspectJ
    # 155 Swt
    print(top5) 
    # 158/587 AspectJ
    # 514 Swt
    print(top10) 
    # 208/587 AspectJ
    # 821 Swt
    print(top20) 
    # 278/587 AspectJ
    # 1256 Swt
    print(MRR) 
    # 0.19069145864854212 AspectJ
    # 0.0936760318790166 Swt
    file_name = 'ranking_label_' + str(alpha) + '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(out, file)

def main_normal(alpha):
    file_ = 'ranking_normal_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    top5 = 0
    top10 = 0
    top20 = 0
    MRR = 0
    for i, bug in enumerate(label):
        x = []
        min = 10000000
        for source in bug:
            if(ranking[i].index(source) < 1):
                count = count + 1
            if min > ranking[i].index(source):
                min = ranking[i].index(source)
            x.append(ranking[i].index(source))
        if(min < 5):
            top5 = top5 + 1
        if(min < 10):
            top10 = top10 + 1
        if(min < 20):
            top20 = top20 + 1
        MRR = MRR + 1 / (min + 1)
        out.append(x)
    MRR = MRR / len(label)
    print(alpha)
    print(count) 
    # 71/587 AspectJ top1
    # 111/1044 Tomcat
    print(top5) 
    print(top10) 
    print(top20) 
    print(MRR) 
    file_name = 'ranking_label_normal_' + str(alpha) + '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(out, file)


if __name__ == '__main__':
    main(0)
    main_normal(0)
    main(0.1)
    main_normal(0.1)
    main(0.2)
    main_normal(0.2)
    main(0.3)
    main_normal(0.3)
    main(0.4)
    main_normal(0.4)
    main(0.5)
    main_normal(0.5)
    main(0.6)
    main_normal(0.6)
    main(0.7)
    main_normal(0.7)
    main(0.8)
    main_normal(0.8)
    main(0.9)
    main_normal(0.9)
    main(1)
    main_normal(1)
