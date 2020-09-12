import pickle
from datasets import DATASET

def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
    print(len(src_files))
    print(len(bug_reports))


if __name__ == '__main__':
    main()
