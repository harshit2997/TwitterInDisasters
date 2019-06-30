import json
import os
from nltk import *
from data_helpers import clean_str

def get_stop():
	stoplist=[]
	fstop=open('stopwords','r')
	for l in fstop:
		if l[0]!='\n':
			l=l[:-1]
			stoplist.append(l.lower())
	fstop.close()
	return stoplist

def clean(a,stoplist):
	#print "h"
	a=clean_str(a)
	sent=a.split()
	temp=[]
	stemmer = PorterStemmer()
	for w in sent:
		fl=0
		fl2=1
		for x in w:
			if  x not in ['0','1','2','3','4','5','6','7','8','9',' ']:
				fl=1
				break
		for x in w:
			if x=='\'' or x=='\"':
				fl2=0
#		if fl2==0 and len(w)<=3:
#			continue
		if f and w!=' '  and w not in ['.',',','\'','\"','/','\\','!'] :#and w not in stoplist:
			temp.append(stemmer.stem(w))
	mod_s=' '.join(temp)
	return mod_s

stemmer=PorterStemmer()

incident = "fire"

f=open("{}_test.json".format(incident),'r')

stoplist=get_stop()

os.chdir ("./{}".format(incident))


for l in f:
	j=json.loads(l)
	text=j["text"]
	id=str(j["id"])
	newf=open(str(id),'w+')
	x=0
	s=""
	while x<len(text):
		if x<len(text)-3 and text[x:x+4]=='http' :

			while text[x]!=' ' and  x<len(text)-1:
				x+=1


		elif x<len(text)-1 and text[x:x+2].lower()=='rt' and (text[x-1]==" " or x==0) :
			while text[x]!=' ' and  x<len(text)-1:
				x+=1

		elif x<len(text)-1 and text[x:x+2].lower()=='..' :
			while text[x]!=' ' and  x<len(text)-1:
				x+=1

		elif x<len(text) and (text[x]=='@') :

			while text[x]!=' ' and  x<len(text)-1:
					x+=1

		elif x<len(text) and text[x]=='#':
			while text[x]=='#' and  x<len(text)-1:
					x+=1


		elif x<len(text)-4 and (text[x:x+5]=='&amp;') :

			s=s+' and '
			x+=4

		else:
			s=s+text[x]			
		x+=1

	temp_json=j
	if "entities" in temp_json.keys() and "hashtags" in temp_json["entities"].keys():
		hash_list = temp_json["entities"]["hashtags"]
		for hashtag in hash_list:
			strtemp = hashtag["text"]
			s=s+" "+strtemp

	#s=clean_str(s)
	'''	
	try:
		mod_s=clean(s.strip().lower(),stoplist)
		wl=mod_s.split()
		wln=[]
		for w in wl:
			wln.append(stemmer.stem(w))
		mod_s=' '.join(wln)
		newf=open(str(j['id']),'w+')
		newf.write(mod_s)
		newf.close()
	except:
		print str(j['id'])
	'''


	try:
		mod_s=clean(s.strip().lower(),stoplist)
		if mod_s!='':
			newf.write(mod_s)
			print str(mod_s)
			newf.close()
		else:
			print "del"
			newf.close()
			os.remove(str(id))				
	except:
		newf.close()
		os.remove(str(id))

os.chdir("../")
f.close()