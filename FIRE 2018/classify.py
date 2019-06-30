import os
import pickle
from data_helpers import *
from nltk import *
from final_pos_words import pos_word_set

lemmatizer = WordNetLemmatizer()
stemmer= PorterStemmer()

output=open("output",'a+')
probabilities=open("probabilities",'r+')

ref_ids=os.listdir("./dev/")

negwf=open("neg_words",'r')
neg_words=set()
for l in negwf:
	l=l[:-1]
	neg_words.add(stemmer.stem(l))

pos_words=pos_word_set()

#print pos_words
print neg_words

#negl=['hope','must','should','sympathy','sympathize','sympathise','sorry','ensure','thank','thankyou','thanks','gratitude','please','pls','empathy','empathize','empathise','political','politics','video','photo','feeling','feel','images','image','grief','sad','sadness','god','omg','condolences	','afraid','scared','fear','sorrow','pity','bad','pray','prayer','felt','think','thought','heart','peace','soul','bless','concern','worried','worry','anxious','anxiety','tension','tensed','heartily','heartless','blame','ruthless','cruel','happy','appreciate','appreciable','appreciation','proud','hats','hatsoff']

i=0
for line in probabilities:
	line=line[:-1]
	li= line.split('\t')
	if float(li[0])>=0.80:
		temp=clean_str(li[2]).split()
		if ('god' not in temp) and ('omg' not in temp) and ('sad' not in temp) and ('pls' not in temp) and ('am' not in temp) and ('you' not in temp) and ('we' not in temp) and ("i\'m" not in temp) and ('my' not in temp) and ('plz' not in temp) and ('i' not in temp):
			temp=stopword([temp])[0]
			#print set(temp).intersection(neg_words)
			if len(set(temp).intersection(pos_words))>1 and len(set(temp).intersection(neg_words))==0:
				output.write(line+'\n')
	elif (li[1] in ref_ids):
		output.write(line+'\n')

probabilities.close()
output.close()