import pickle
import json
from datasets import DATASET
from collections import OrderedDict

# with open(DATASET.root / 'Aspectj_name.json', 'rb') as file:
#     src_name1 = json.load(file)
# with open(DATASET.root / 'preprocessed_src_id.json', 'rb') as file:
#     src_name2 = json.load(file)

# print(len(src_name1))
# print(len(src_name2))
# out = []
# for x in src_name2:
#     out.append(x.split("/")[-1])
# print(src_name2[146: 149])
# for i, x in enumerate(out):
#     print(x, x in src_name1)
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
    print(src.exact_file_name)
    print(src.file_name)
    print(src.class_names)
    data_source_reports.append(
        src.id.replace("\\", "/")
    )
with open(DATASET.root / 'preprocessed_src_id.json', 'w') as file:
    json.dump(data_source_reports, file)
with open(DATASET.root / 'preprocessed_reports_id.json', 'w') as file:
    json.dump(data_bug_reports, file)
print(len(data_bug_reports))

print(len(data_source_reports))
