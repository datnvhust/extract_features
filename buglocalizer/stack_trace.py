import pickle
import json
import numpy as np
from collections import OrderedDict

from datasets import DATASET


def get_traces_score(src_files, bug_reports):
    
    all_file_names = set(s.exact_file_name.split(' ')[-1] for s in src_files.values())
    all_scores = []
    for report in bug_reports.values():
        print(report.commit)
        scores = []
        
        stack_traces = report.stack_traces
        # print(stack_traces)
        final_st = []
        for trace in stack_traces:
            if trace[1] == 'Unknown Source':
                final_st.append((trace[0].split('.')[-2].split('$')[0], trace[0].strip()))
            elif trace[1] != 'Native Method':
                final_st.append((trace[1].split('.')[0].replace(' ', ''), trace[0].strip()))
        
        stack_traces = OrderedDict([(file, package) for file, package in final_st
                                    if file in all_file_names])
        # print(stack_traces)
        
        for src in src_files.values():
            file_name = src.exact_file_name.split(' ')[-1]
            # print(file_name)
            # print(src.package_name)
            if src.package_name:
                if file_name in stack_traces and src.package_name in stack_traces[file_name]:
                    scores.append(1 / (list(stack_traces).index(file_name) + 1))
                    
                else:
                    # If it isn't the exact source file based on it's package name
                    scores.append(0)
            # If it doesn't have a package name
            elif file_name in stack_traces:
                scores.append(1 / (list(stack_traces).index(file_name) + 1))
            else:
                scores.append(0)
        
        all_scores.append(scores)
 
    return all_scores
    
    
def main():
    #custom max rank = 10 and add set C
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
        
    all_scores = get_traces_score(src_files, bug_reports)
    print(len(all_scores))
    print(len(all_scores[0]))
    print(np.max(all_scores))
    print(np.min(all_scores))
    with open(DATASET.root / 'stack_trace.json', 'w') as file:
        json.dump(all_scores, file)


if __name__ == '__main__':
    main()
        
