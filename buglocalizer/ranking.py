import json
from datasets import DATASET
import numpy as np

def main(alpha):
    file_ = 'module3_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        module = json.load(file)
    out = []
    for m in module:
        temp = np.argsort(m).tolist()
        temp.reverse()
        out.append(temp)
    
    file_name = 'ranking_' + str(alpha) +  '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(out, file)

def main_normal(alpha):
    file_ = 'module3_normal_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        module = json.load(file)
    
    out = []
    for m in module:
        temp = np.argsort(m).tolist()
        temp.reverse()
        out.append(temp)
    
    file_name = 'ranking_normal_' + str(alpha) +  '.json'
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

    # myList = [1, 2, 3, 100, 5]
    # print(np.argsort(myList).tolist().reverse())