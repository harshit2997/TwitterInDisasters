import os
#from data_helpers import clean_str
from nltk import *
import operator
import numpy as np
import math
import operator
from data_helpers import load_data


stemmer= PorterStemmer()

os.chdir ("./Data/Train/")
disasters = os.listdir(".")

dev_sentences = []
test_sentences = []
words_dev = set()
words_test = set()

target = disasters[5]

for disaster in disasters:
	os.chdir("./{}/".format(disaster))
	incidents = os.listdir (".")
	for incident in incidents:
		os.chdir("./{}/".format(incident))
		tweets = os.listdir (".")
		for tweet in tweets:
			temp_sentence=[]
			ftweet = open (tweet,'r')
			for line in ftweet:
				if line[-1]=='\n':
					line=line[:-1]
				if (len(line)==0):
					continue
				wlist=line.split()
				for word in wlist:
					wstem=stemmer.stem(word)
					if (len(wstem)>3):
						temp_sentence.append(wstem)
			ftweet.close()
			if (disaster == target and temp_sentence!=[]):
				dev_sentences.append(temp_sentence)
			elif (disaster!=target and temp_sentence!=[]):
				test_sentences.append(temp_sentence)
		os.chdir("./../")
	os.chdir("./../")

for sentence in dev_sentences:
	for wstem in sentence:
		words_dev.add(wstem)

for sentence in test_sentences:
	for wstem in sentence:
		words_test.add(wstem)

words_dev=list(words_dev)
words_test=list(words_test)

dfP=np.ones((len(words_dev),len(dev_sentences)))
dfU=np.ones((len(words_dev),len(test_sentences)))

for i in range (len(words_dev)):
	for j in range (len(dev_sentences)):
		dfP[i,j]=dev_sentences[j].count(words_dev[i])

for i in range (len(words_dev)):
	for j in range (len(test_sentences)):
		dfU[i,j]=test_sentences[j].count(words_dev[i])

print "DFP, DFU calculated"
print len(words_dev)
print len(words_test)

N=[]
M=[]

for j in range(len(dev_sentences)):
	M.append(dfP.max(axis=0)[j])

for i in range(len(words_dev)):
	temp=0.0
	for j in range(len(dev_sentences)):
		temp+=float(float(dfP[i][j])/float(M[j]))
	N.append(temp)

total=sum(N)

print "N and total calculated"

s={}
count=0
for i in range(len(words_dev)):
	sdfp = dfP.sum(axis=1)[i]
	if sdfp<=1:
		continue
	lt=math.log(float(len(dev_sentences)+len(test_sentences))/float(sdfp+dfU.sum(axis=1)[i]))
	p=(lt*float(N[i]))/float(total)	
	s[words_dev[i]]=p
	count+=1

print "Scores calculated"

sorted_s= sorted(s.items(), key=operator.itemgetter(1))
sorted_s.reverse()

print "Scores sorted"

keywords=[]
i=0
for t in sorted_s:
	if (i>100):
		break
	if len(t[0])>3 and 	t[0][0]!='\\' and t[0]:
		keywords.append(t)
		i+=1
print "Number of keywords: " + str(len(keywords))
print target
print keywords