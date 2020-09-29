import pickle
import json
from datasets import DATASET
from collections import OrderedDict

with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
    src_files = pickle.load(file)
with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
    bug_reports = pickle.load(file)
data_bug_reports = []
for bug in bug_reports.values():
    data_bug_reports.append(
        bug.id
    )
    bug_detail = {}

data_source_reports = []
for src in src_files.values():
    data_source_reports.append(
        src.id.replace("\\", "/")
    )
with open(DATASET.root / 'preprocessed_src_id.json', 'w') as file:
    json.dump(data_source_reports, file)
with open(DATASET.root / 'preprocessed_reports_id.json', 'w') as file:
    json.dump(data_bug_reports, file)
print(len(data_bug_reports))
