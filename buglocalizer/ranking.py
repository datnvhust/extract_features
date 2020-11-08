import json
from datasets import DATASET
import numpy as np

def main():
    with open(DATASET.root / 'module3.json', 'rb') as file:
        module = json.load(file)
    out = []
    for m in module:
        temp = np.argsort(m).tolist()
        temp.reverse()
        out.append(temp)
    
    with open(DATASET.root / 'ranking.json', 'w') as file:
        json.dump(out, file)

def main_normal():
    with open(DATASET.root / 'module3_normal.json', 'rb') as file:
        module = json.load(file)
    
    out = []
    for m in module:
        temp = np.argsort(m).tolist()
        temp.reverse()
        out.append(temp)
    
    with open(DATASET.root / 'ranking_normal.json', 'w') as file:
        json.dump(out, file)

if __name__ == '__main__':
    main()
    main_normal()

    # myList = [1, 2, 3, 100, 5]
    # print(np.argsort(myList).tolist().reverse())