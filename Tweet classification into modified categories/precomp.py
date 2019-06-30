import os
import math
import pickle
import nltk

incident = "typhoon"
n=6007
os.chdir("./"+incident+"_train")

cwise = [dict() for i in range(9)]
idf = dict()
df= dict()
entropy = dict()

word_set = set()
sentences=[]

stoplist=[]
fstop=open('../stopwords','r')
for l in fstop:
    if l[0]!='\n':
        l=l[:-1]
        stoplist.append(l)
fstop.close()

stemmer = nltk.PorterStemmer()

exclude = []
f_ex = open("../Media Train/"+incident+".jsonmedia")
for l in f_ex:
    line = l.strip()
    exclude.append(str(line))
f_ex.close()

for cls in range(9):
    thiscls=[]
    os.chdir("./"+str(cls))
    fl_temp=os.listdir(".")
    fl = [name for name in fl_temp if name not in exclude]
    for name in fl:
        sentence=[]
        f=open(name,'r')
        for l in f:
            line = l.strip()
            for word in line.split():
                if word not in stoplist and len(word)>2 and word[0] not in ['0','1','2','3','4','5','6','7','8','9','\'',"\"",'/','\\','.',',',';','!',':']:
                    #w_stem=stemmer.stem(word)
                    w_stem=word
                    word_set.add(w_stem)
                    sentence.append(w_stem)
        f.close()
        thiscls.append(sentence)
    sentences.append(thiscls)
    os.chdir("../")

vocabulary = list(word_set)

#print len(vocabulary)

for word in vocabulary:
    df[word]=0
    #idf[word]=0.0
    #entropy[word]=0
    for i in range(0,9):
        cwise[i][word]=0

for cln in range(9):
    cur_class=sentences[cln]
    for sentence in cur_class:
        sent_set = set(sentence)
        for word in sentence:
            cwise[cln][word]+=1
        for word in sent_set:
            df[word]+=1
            

for word in vocabulary:
    if df[word]>0.0:
        idf[word]=math.log10(float(n)/float(df[word]))
        #idf[word]=(float(n)/float(df[word]))
    total=0
    for cln in range(9):
        total+=cwise[cln][word]
    if total>0:
        accum=0.0
        for cln in  range(9):
            temp =float(cwise[cln][word])/float(total)
            if temp>0:
                accum = float(accum) - float((float(temp))* math.log(float(temp),2)) 
        entropy[word] = accum
    
max_entropy = entropy[entropy.keys()[0]]
for word in entropy.keys():
    max_entropy=max(max_entropy, entropy[word])

for word in entropy.keys():
    entropy[word] = float(max_entropy - entropy[word])/float(max_entropy)

f_idf = open ("idf",'wb+')
f_entropy = open ("entropy",'wb+')
f_cwise = open ("cwise" , 'wb+')

pickle.dump(idf , f_idf)
pickle.dump(entropy , f_entropy)
pickle.dump(cwise , f_cwise)

f_idf.close()
f_entropy.close()
f_cwise.close()

print entropy

max_len=-1

ct=0

for cln in sentences:
    for sentence in cln:
        max_len = max (max_len, len(sentence))
        ct+=1

print max_len
print str(ct)






