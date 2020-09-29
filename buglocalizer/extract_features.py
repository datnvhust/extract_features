import json
from datasets import DATASET

def main():
    with open(DATASET.root / 'text_structure.json', 'rb') as file:
        text_structure = json.load(file)['data']
    with open(DATASET.root / 'stack_trace.json', 'rb') as file:
        stack_trace = json.load(file)
    with open(DATASET.root / 'version_history.json', 'rb') as file:
        version_history = json.load(file)
    with open(DATASET.root / 'hub.json', 'rb') as file:
        hub = json.load(file)
    with open(DATASET.root / 'similar_report.json', 'rb') as file:
        similar_report = json.load(file)
    keys_hub = hub.keys()
    extract_features = []
    for i, bug in enumerate(text_structure):
        bugs = []
        for j, source in enumerate(bug):
            source_features = []
            source_features.append(text_structure[i][j])
            source_features.append(stack_trace[i][j])
            source_features.append(version_history[i][j])
            if str(j) in keys_hub:
                source_features.append(hub[str(j)])
            else:
                source_features.append(0)
            source_features.append(similar_report[i][j])

            bugs.append(source_features)
        extract_features.append(bugs)
    
    with open(DATASET.root / 'extract_features.json', 'w') as file:
        json.dump(extract_features, file)



if __name__ == '__main__':
    main()

# normalize theo từng bug