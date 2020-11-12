import preprocessing
import dump
import label
import module1
import module2
import module3
import ranking
import ranking_label_1

print("Preprocessing...")
preprocessing.main()

# print("Dump...")
# dump.main()

print("Label...")
label.load()

print("Module1...")
module1.main()

print("Module2...")
module2.main()

print("Module3...")
module3.load()

print("Rank...")
ranking.load()

print("Rank label...")
ranking_label_1.load()


"""
sum + des (NN)
0 normal
47
116
153
206
0.19812968628409736
0
50
116
151
198
0.1994551554035991
0.1 normal
53
114
159
210
0.21063612891147676
0.1
57
120
158
201
0.21301086878594785
0.2 normal
58
118
160
210
0.21698682532060076
0.2
60
126
162
205
0.22386107877432654
0.3 normal
65
125
163
209
0.23204843015772741
0.3
63
127
162
210
0.23149874795308098
0.4 normal
68
126
162
207
0.23689467623120097
0.4
69
133
171
210
0.24094418902143358
0.5 normal
64
125
169
204
0.23324528221340246
0.5
69
130
167
210
0.24247042736922902
0.6 normal
68
128
168
201
0.23764399522358878
0.6
72
128
171
208
0.24671002448242757
0.7 normal
71
130
172
200
0.2427307029282842
0.7
71
131
175
205
0.2441933899572957
0.8 normal
72
129
168
197
0.2444871149802068
0.8
72
136
170
201
0.24486465279118427
0.9 normal
70
130
169
196
0.23759775278027803
0.9
74
130
168
201
0.24534563153191016
1 normal
71
124
166
201
0.23799980442461188
1
71
124
166
201
"""

"""
No_test
0 normal
44
105
139
186
0.2010395119151955
0
46
101
140
183
0.20058428578284468
0.1 normal
47
104
145
190
0.21163383873535413
0.1
51
108
146
186
0.21309958037442994
0.2 normal
53
110
149
192
0.22274143257628845
0.2
53
114
151
192
0.22287504202082284
0.3 normal
61
116
153
193
0.23839322514504532
0.3
56
116
151
196
0.2323384922073201
0.4 normal
59
117
151
194
0.2371795541524923
0.4
63
122
160
198
0.24407638653757166
0.5 normal
58
116
158
193
0.23718451906939586
0.5
62
120
157
197
0.24525358005466164
0.6 normal
62
119
157
189
0.24288759639477966
0.6
63
119
161
193
0.2480584935895753
0.7 normal
63
122
161
188
0.24581105523880875
0.7
66
123
164
192
0.25171240157917324
0.8 normal
67
122
159
188
0.2515957743022709
0.8
67
128
160
189
0.2517798856741951
0.9 normal
66
124
160
187
0.24667939490282595
0.9
67
123
160
190
0.25029645306950443
1 normal
68
121
157
192
0.2508868358819756
1
68
121
157
192
0.2508868358819756
"""