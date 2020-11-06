import json
from datasets import DATASET

def main(alpha):
    with open(DATASET.root / 'module1.json', 'rb') as file:
        module1 = json.load(file)
    with open(DATASET.root / 'module2.json', 'rb') as file:
        module2 = json.load(file)
    
    output = []
    for i, bug in enumerate(module1):
        x = []
        m2 = module2[i]
        for j, source in enumerate(bug):
            x.append(source * alpha + ( 1 - alpha ) * m2[j])
        output.append(x)
    
    with open(DATASET.root / 'module3.json', 'w') as file:
        json.dump(output, file)

if __name__ == '__main__':
    main(0.3)