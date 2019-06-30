import os
from data_helpers import *
import operator
import pickle
import os
import pickle
from data_helpers import *
from nltk import *

lemmatizer = WordNetLemmatizer()
stemmer= PorterStemmer()


def neg_word_set():
	probabilities=open("probabilities",'r+')
	word_freq=dict()
	neg_words=set()

	for line in probabilities:
		line=line[:-1]
		li= line.split('\t')
		if float(li[0])<=0.80 and float(li[0])>=0.70:
			temp=clean_str(li[2]).split()
			temp=stopword([temp])[0]
			for word in temp:
				if word in word_freq.keys():
					word_freq[word]+=1
				else:
					word_freq[word]=1

	word_freq_sorted= sorted(word_freq.items(), key=operator.itemgetter(1))
	word_freq_sorted.reverse()

	for t in word_freq_sorted[:500]:
		if t[1]>=5 and len(t[0])>3:
			neg_words.add(t[0])

#	print neg_words
#	print len(neg_words)
	return neg_words

'''
neg_words_file=open("final_neg_words",'wb')
pickle.dump(neg_words,neg_words_file)
neg_words_file.close()
'''