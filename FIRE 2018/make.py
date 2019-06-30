import json
import os
from data_helpers import clean_str

i=0
f=open('nepal-quake-sample-fact-checkable-tweets.txt','r')
os.chdir("./dev/")
for l in f :
	text=l[22:len(l)-1]
	id=l[:18]

	newf=open(id,'w+')
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

		elif x<len(text) and (text[x]=='@' or text[x]=='#') :

			while text[x]!=' ' and  x<len(text)-1:
				x+=1


		elif x<len(text)-4 and (text[x:x+5]=='&amp;') :

			s=s+' and '
			x+=4
			
		elif x<len(text) and (text[x]=='&') :

			s=s+' and '
			x+=1						
					
		else:
			s=s+text[x]		
		x+=1
	s=clean_str(s)
	newf.write(s.strip().lower())
	print s.strip().lower()
	print
	newf.close()
	i+=1

print str(i)

'''
		elif x<len(text)-3 and (text[x:x+4].lower()=='hnfn' or text[x:x+4].lower()=='rofl') :

			while text[x]!=' ' and  x<len(text)-1:
				x+=1

		elif x<len(text)-2 and (text[x:x+3].lower()=='lol' or text[x:x+4].lower()=='rip') :

			while text[x]!=' ' and  x<len(text)-1:
				x+=1
'''

