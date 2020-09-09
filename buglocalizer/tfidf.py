from math import log
class TFIDFVectorizer():
    def __init__(self, k=1.5, b=0.75):
        self.k = k
        self.b = b

    def tf(self,word,doc, doc_list):
        all_num=sum([doc[key] for key in doc])
        avg = 0
        for vb in doc_list:
            avg += sum([vb[key] for key in vb])
        avg = avg/len(doc_list)
        return (doc[word]*(self.k + 1))/(doc[word] + self.k*(1 - self.b + self.b*all_num/avg))

    def idf(self, word,doc_list):
        all_num=len(doc_list)
        word_count=0
        for doc in doc_list:
            if word in doc:
                word_count+=1
        return log((all_num+1)/(word_count+0.5))

    def tfidf(self, word,doc,doc_list):
        score = self.tf(word,doc, doc_list)*self.idf(word,doc_list)
        return score

if __name__=='__main__':
    doc1={'mik1':28,'aa':16,'web':14,'be':2,'python':1}
    doc2={'mik2':21,'ab':11,'web':14,'chal':5}
    doc3={'mik3':126,'bc':116,'web':74,'lelo':12,'foot':1}
    doc4={'mik4':8,'cd':3,'arbit':2,'da':1,'fork':1}
    doc_list=[doc1,doc2,doc3,doc4]
    tfidf = TFIDFVectorizer()
    for doc in doc_list:
        for word in doc:
            print( word,tfidf.tfidf(word,doc,doc_list))
import pandas as pd 


# data = pd.read_csv('AspectJ.csv',  index_col=False)
# doc_list = data['summary']
# print(doc_list)