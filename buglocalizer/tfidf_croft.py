from math import log
class TFIDFVectorizer():
    def tf(self,word,doc, doc_list):
        return log(doc[word]) + 1

    def idf(self, word,doc_list):
        all_num=len(doc_list)
        word_count=0
        for doc in doc_list:
            if word in doc:
                word_count+=1
        return log((all_num)/(word_count))

    def tfidf(self, word,doc,doc_list):
        score = self.tf(word,doc, doc_list)*self.idf(word,doc_list)
        return score

if __name__=='__main__':
    doc1={'mik1':28,'aa':16,'web':14,'be':2,'python':1}
    doc2={'mik2':21,'ab':11,'web':14,'chal':5}
    doc3={'mik3':126,'bc':116,'web':74,'lelo':12,'foot':1}
    doc4={'mik4':8,'cd':3,'arbit':2,'da':1,'fork':1}
    doc_list=[doc1,doc2,doc3,doc4]
    # doc_list=[doc1]
    tfidf = TFIDFVectorizer()
    for doc in doc_list:
        for word in doc:
            print( word,tfidf.tfidf(word,doc,doc_list))
import pandas as pd 


# data = pd.read_csv('AspectJ.csv',  index_col=False)
# doc_list = data['summary']
# print(doc_list)