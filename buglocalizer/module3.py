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
    
    file_name = 'module3_' + str(alpha) + '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(output, file)

def main_normal(alpha):
    with open(DATASET.root / 'module1.json', 'rb') as file:
        module1 = json.load(file)
    with open(DATASET.root / 'module2_normal.json', 'rb') as file:
        module2 = json.load(file)
    
    output = []
    for i, bug in enumerate(module1):
        x = []
        m2 = module2[i]
        for j, source in enumerate(bug):
            x.append(source * alpha + ( 1 - alpha ) * m2[j])
        output.append(x)
    file_name = 'module3_normal_' + str(alpha) + '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(output, file)
def load():
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