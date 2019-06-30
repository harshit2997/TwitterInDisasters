import pickle
import numpy as np

fwd=open("words_dev_set",'rb')
words_dev=pickle.load(fwd)
fwd.close()

fwt=open("words_test_set",'rb')
words_test=pickle.load(fwt)
fwt.close()

ftt=open("test_tweets",'rb')
test_tweets=pickle.load(ftt)
ftt.close()

fds=open("dev_sentences",'rb')
dev_sentences=pickle.load(fds)
fds.close()

fts=open("test_sentences",'rb')
test_sentences=pickle.load(fts)
fds.close()

fp=open("prob",'rb')
prob=pickle.load(fp)
fp.close()
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																							
vocab=list(words_test)

v=len(vocab)

#print "diff is "+ str(vocab.difference(words_test))
#all_sentences=dev_sentences+test_sentences

d=len(test_sentences)
df=np.zeros((v,d),dtype=float)

print ("Building DF matrix")

for i in range (v):
	for j in range (d):
		df[i,j]=test_sentences[j].count(vocab[i])

np.savez_compressed('doc_frequency', a=df)

print ("DF matrix built and stored.")