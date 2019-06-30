import os
from data_helpers import *
import operator
import pickle


def pos_word_set():
	word_freq=dict()

	f=open("dev_sentences",'r')
	sentences=pickle.load(f)
	for sent in sentences:
		for word in sent:
			if word in word_freq.keys():
				word_freq[word]+=1
			else:
				word_freq[word]=1

	word_freq_sorted= sorted(word_freq.items(), key=operator.itemgetter(1))
	word_freq_sorted.reverse()

	test_words=set()

	for t in word_freq_sorted:
		if t[1]>=2 and len(t[0])>3 and t[0] not in ['humanitarian','hand','need','work','rais','done','india','pakistan','nepal','good','great']:
			test_words.add(t[0])
	test_words.add('magnitud')

#	print test_words
#	print len(test_words)
	return test_words

'''
test_words_file=open("final_test_words",'wb')
pickle.dump(test_words,test_words_file)
test_words_file.close()
'''