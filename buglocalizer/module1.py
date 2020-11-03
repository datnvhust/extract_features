import pickle
from datasets import DATASET

def getModule1(src_files, bug_reports):
    for report in bug_reports.values():
        print(report.id)

def main():
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    getModule1(src_files, bug_reports)

if __name__ == '__main__':
    main()