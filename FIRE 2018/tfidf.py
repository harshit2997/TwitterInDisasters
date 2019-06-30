from __future__ import division

from data_helpers import load_data
from nltk.stem import WordNetLemmatizer
import numpy as np
import math
import operator
from w2v import train_word2vec
from scipy.spatial import distance
import pickle

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Convolution1D, Embedding
from keras.layers.merge import Concatenate
from keras.datasets import imdb
from keras.preprocessing import sequence

embedding_dim=50
min_word_count = 0
context = 3

[x, y, vocabulary, vocabulary_inv_list, sequence_length,sentences,raw_test]=load_data()
vocabulary_inv = {key: value for key, value in enumerate(vocabulary_inv_list)}

dev_sentences=sentences[:84]
x_dev=x[:84]
test_sentences=sentences[84:]
x_test=x[84:]
print ("size of test is   "+str(len(x_test)))
score={}
lemmatizer = WordNetLemmatizer()


dev_sentences2=[]
test_sentences2=[]

words_dev=set()

for sent in dev_sentences:
	temp=[]
	for w in sent:
		temp.append(w)
		words_dev.add(w)
	if temp!=[]:
		dev_sentences2.append(temp)

#empty=[]
#u=0
test_tweets=[]
i=0
words_test=set()
for sent in test_sentences:
	temp=[]
	for w in sent:
		temp.append(w)
		words_test.add(w)
	if temp!=[]:
		test_sentences2.append(temp)
		test_tweets.append(raw_test[i])
	i+=1
	#else:
	#	empty.append(u)
	#u+=1

#print empty

#print "Empty:"
#print str(len(dev_sentences)-len(dev_sentences2))
#print str(len(test_sentences)-len(test_sentences2))
#dev_sentences2.remove([])

words_dev=list(words_dev)
words_test=list(words_test)

dfP=np.ones((len(words_dev),len(dev_sentences2)))
dfU=np.ones((len(words_dev),len(test_sentences2)))


for i in range (len(words_dev)):
	for j in range (len(dev_sentences2)):
		dfP[i,j]=dev_sentences2[j].count(words_dev[i])

for i in range (len(words_dev)):
	for j in range (len(test_sentences2)):
		dfU[i,j]=test_sentences2[j].count(words_dev[i])


#dfP=[[dev_sentences2[i].count(words_dev[j]) for i in range(len(dev_sentences2))] for j in range (len(words_dev))]
#dfU=[[test_sentences2[i].count(words_dev[j]) for i in range(len(test_sentences2))] for j in range (len(words_dev))]

N=[]

for i in range(len(words_dev)):
	temp=0
	for j in range(len(dev_sentences2)):
		temp+=float(float(dfP[i][j])/float(dfP.max(axis=0)[j]))
	N.append(temp)

total=sum(N)

s={}
count=0
for i in range(len(words_dev)):
	lt=math.log(float(len(dev_sentences2)+len(test_sentences2))/float(dfP.sum(axis=1)[i]+dfU.sum(axis=1)[i]))
	p=(lt*float(N[i]))/float(total)
	if dfP.sum(axis=1)[i]>1:	
		s[words_dev[i]]=p
		count+=1

sorted_s= sorted(s.items(), key=operator.itemgetter(1))
sorted_s.reverse()
keywords=[]
for t in sorted_s:
	if len(t[0])>3 and 	t[0][0]!='\\' and t[0]:
		keywords.append(t)
print "Number of keywords: " + str(len(keywords))
print keywords

print "Dev vocab: " +str(len(words_dev))
print "Test vocab: " + str(len(words_test))


input_shape = (1,)
model_input = Input(shape=input_shape)

model_output = Embedding(len(vocabulary_inv), embedding_dim, input_length=1, name="embedding")(model_input)

model=Model(model_input,model_output)

embedding_weights = train_word2vec(x, vocabulary_inv, num_features=embedding_dim, min_word_count=min_word_count, context=context)

embedding_layer = model.get_layer("embedding")
weights = np.array([v for v in embedding_weights.values()])
embedding_layer.set_weights([weights])


repr=np.zeros((1,embedding_dim))
wt_accum=0.0
for t in keywords:
	if t[0] not in ['hand','more','touch','than','done','humanitarian','great','district','mani','donat','name','nation','peopl','establish','break','govern','rais','charg','help','colleg','news']:
		wt_accum+=(t[1]/float(keywords[0][1]))
		npout = model.predict( np.array([vocabulary[t[0]]]), batch_size=1)
		repr+=(npout[0]*(t[1]/float(keywords[0][1])))
repr/=float(wt_accum)

print str(wt_accum)


test_features=[]

for sent in x_test:
	count=0
	temp=np.zeros((1,1,embedding_dim))
	for w in sent:
		if w!=0:
			count+=1
			npout = model.predict( np.array([w]), batch_size=1)
			temp=temp+npout
	if count!=0:
		temp/=float(count)
		test_features.append(temp[0])
	#else:
	#	print "Blank sentence after "+str(len(test_features))
	#	print "Sentence:"
	#	print sent

#print len(test_sentences2)-len(test_features)

sim=[]
prob=[]
for feat in test_features:
	x=1.0-distance.cosine(feat,repr)
	sim.append(x)
m=max(sim)
nc=0
i=0
fpn=open("probabilities",'a+')
for x in sim:
	prob.append(x/float(m))
	#if x<0.7:
	#	nc+=1
	#	fpn.write(str(test_tweets[i])+'\n')
	#i+=1

#fpn.close()
#print str(nc)
print str(m)
indices=list(np.argsort(np.array(prob)))[::-1]
for x in indices:
	line= str(prob[x])+'\t'+str(test_tweets[x][0])+'\t'+str(test_tweets[x][1])+'\n'
	fpn.write(line)
fpn.close()

#for i in range(100,200):
#	print test_sentences2[i]
#	print sim[i]

fwd=open("words_dev_set",'wb')
pickle.dump(set(words_dev),fwd)
fwd.close()

fwt=open("words_test_set",'wb')
pickle.dump(set(words_test),fwt)
fwt.close()

ftt=open("test_tweets",'wb')
pickle.dump(test_tweets,ftt)
ftt.close()

fds=open("dev_sentences",'wb')
pickle.dump(dev_sentences2,fds)
fds.close()

fts=open("test_sentences",'wb')
pickle.dump(test_sentences2,fts)
fds.close()

fp=open("prob",'wb')
pickle.dump(prob,fp)
fp.close()







