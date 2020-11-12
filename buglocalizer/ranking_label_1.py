import json
from datasets import DATASET
import numpy as np

def main(alpha):
    file_ = 'ranking_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    top5 = 0
    top10 = 0
    top20 = 0
    MRR = 0
    for i, bug in enumerate(label):
        x = []
        min = 10000000
        for source in bug:
            if(ranking[i].index(source) < 1):
                count = count + 1
            if min > ranking[i].index(source):
                min = ranking[i].index(source)
            x.append(ranking[i].index(source))
        if(min < 5):
            top5 = top5 + 1
        if(min < 10):
            top10 = top10 + 1
        if(min < 20):
            top20 = top20 + 1
        MRR = MRR + 1 / (min + 1)
        out.append(x)
    MRR = MRR / len(label)
    print(alpha, 'normal')
    print(count) 
    # 63/587 AspectJ
    # 155 Swt
    print(top5) 
    # 158/587 AspectJ
    # 514 Swt
    print(top10) 
    # 208/587 AspectJ
    # 821 Swt
    print(top20) 
    # 278/587 AspectJ
    # 1256 Swt
    print(MRR) 
    # 0.19069145864854212 AspectJ
    # 0.0936760318790166 Swt
    file_name = 'ranking_label_' + str(alpha) + '.json'
    with open(DATASET.root / file_name, 'w') as file:
        json.dump(out, file)

def main_normal(alpha):
    file_ = 'ranking_normal_' + str(alpha) + '.json'
    with open(DATASET.root / file_, 'rb') as file:
        ranking = json.load(file)
    with open(DATASET.root / 'name_src_label_1.json', 'rb') as file:
        label = json.load(file)
    out = []
    count = 0 
    top5 = 0
    top10 = 0
    top20 = 0
    MRR = 0
    for i, bug in enumerate(label):
        x = []
        min = 10000000
        for source in bug:
            if(ranking[i].index(source) < 1):
                count = count + 1
            if min > ranking[i].index(source):
                min = ranking[i].index(source)
            x.append(ranking[i].index(source))
        if(min < 5):
            top5 = top5 + 1
        if(min < 10):
            top10 = top10 + 1
        if(min < 20):
            top20 = top20 + 1
        MRR = MRR + 1 / (min + 1)
        out.append(x)
    MRR = MRR / len(label)
    print(alpha)
    print(count) 
    # 71/587 AspectJ top1
    # 111/1044 Tomcat
    print(top5) 
    print(top10) 
    print(top20) 
    print(MRR) 
    file_name = 'ranking_label_normal_' + str(alpha) + '.json'
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

"""
All 587 bug
0 normal
51
122
184
257
0.15983492397062268
0
65
125
177
237
0.1732221698775227
0.1 normal
58
137
201
270
0.1747604589473778
0.1
66
130
186
247
0.18059243927679716
0.2 normal
65
147
204
274
0.1863489056589566
0.2
71
146
199
258
0.19234956170090706
0.3 normal
63
158
208
278
0.19100103445398853
0.3
71
156
206
271
0.201239578793336
0.4 normal
68
165
212
277
0.20041948371494908
0.4
77
163
215
272
0.21273520705999255
0.5 normal
69
163
218
280
0.2034382850106705
0.5
81
176
223
277
0.22015998017691282
0.6 normal
75
165
218
279
0.21148551001181093
0.6
79
178
223
281
0.2194745766768538
0.7 normal
79
169
217
276
0.21607745019831107
0.7
84
177
218
285
0.2245895203484923
0.8 normal
82
170
215
270
0.21765045517931833
0.8
83
174
218
279
0.22318969088593552
0.9 normal
84
172
213
269
0.22074207995539763
0.9
86
175
222
273
0.22570292189031524
1 normal
86
172
218
271
0.22364381995977492
1
86
172
218
271
0.22364381995977492
"""