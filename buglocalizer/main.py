# import nltk
# nltk.download()

import preprocessing
import vsm_similarity
import token_matching
import stack_trace
import semantic_similarity
import text_structure
import hub
import fixed_bug_reports
import evaluation

#feature giữa từng bug và source (5 giá trị cho các source file)

#features thành mxn vector
# bugs matrix cho source x features 
# preprocessing
# print('Parsing & Preprocessing...')
# preprocessing.main()


# print('Token Matching...')
# token_matching.main()

# print('VSM Similarity...')
# vsm_similarity.main()

# feature 2
# print('Stack Trace...')
# stack_trace.main()

# print('Semantic Similarity...')
# semantic_similarity.main()

# print('Text Structure...')
# text_structure.main()


print('Hub...')
hub.main()

# print('Fixed Bug Reports...')
# fixed_bug_reports.main()

# print('Evaluating...')
# evaluation.main()