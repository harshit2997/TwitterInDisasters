import os
import pickle
from data_helpers import *

os.chdir("./nepal-quake-2015-news-articles/")
fnl=os.listdir(".")

for fn in fnl:
	f=open(fn,'r')
	headline=""
	flag=0
	for l in f:
		if l[:-1]=="<headline>":
			flag=1
			continue
		if l[:-1]=="</headline>":
			flag=0
			headline=headline[:-1]
			break
		if flag==1:
			headline+=l[:-1]+" "
	#print headline
	f.close()
	headline=clean_str(headline)
	tokens=headline.split()
	os.chdir("../")
	stop_tokens=stopword_2([tokens])[0]
	os.chdir("./nepal-quake-2015-news-articles/")
	headline=' '.join(stop_tokens)
	os.chdir("../headlines/")
	fh=open(fn,'w+')
	fh.write(headline)
	fh.close()
	os.chdir("../nepal-quake-2015-news-articles/")

for fn in fnl:
	f=open(fn,'r')
	text=[]
	flag=0
	for  l in f:
		if l[:-1]=='<text>':
			flag=1
			continue
		if l=='</text>' or l[:-1]=='</text>':
			flag=0
			break
		if flag==1 and l[0]!='\n':
			line=l[:-1]
			for s in line.split("."):
				text.append(s)
	f.close()
	os.chdir("../text/")
	os.system("mkdir {}".format(fn))
	os.chdir("./{}".format(fn))
	sent_count=0
	first=""
	second=""
	third=""
	for s in text:
	    txt=clean_str(s)
	    tokens=txt.split()
	    if tokens==[]:
	    	continue
	    os.chdir("../../")
	    try:
	    	stop_tokens=stopword_2([tokens])[0]
	    except:
	    	print str(fn)
	    	print str(sent_count)
	    	print tokens
	    os.chdir("./text/{}".format(fn))
	    txt=' '.join(stop_tokens)
	    f=open(str(sent_count),'w+')
	    f.write(str(txt))
	    f.close()
	    if sent_count==0:
	    	first=txt
	    elif sent_count==1:
	    	second=txt
	    elif sent_count==2:
	    	third=txt
	    sent_count+=1
	if len(text)>2:
		added=". "+first+". "+second+". "+third+"."
	elif len(text)>1:
		added=". "+first+". "+second+"."
	else:
		added=". "+first+"."
	os.chdir("../../headlines")
	fh=open(fn,'a+')
	fh.write(first)

	fh.close()
	os.chdir("../nepal-quake-2015-news-articles/")



			








