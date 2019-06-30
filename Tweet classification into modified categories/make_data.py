import os
import xlrd 
from data_helpers import clean_str
import json

incident = "typhoon"
  
excel_train = "./train.xlsx"
excel_test = "./test.xlsx" 
  
wb_train = xlrd.open_workbook(excel_train)
wb_test = xlrd.open_workbook(excel_test) 
 
sheet_train = wb_train.sheet_by_index(5)  
sheet_test = wb_test.sheet_by_index(5)  

ntrain = sheet_train.nrows
ntest = sheet_test.nrows

train_json = open('./train_json/'+incident+'.json','r')
test_json = open('./test_json/'+incident+'.json','r')

os.chdir("./"+incident+"_train")

for i in range(9):
	os.system("rm -rf "+str(i))
	os.system("mkdir "+str(i))

ln=1

for line in train_json:
	if (len(line.strip())<2):
		continue
	parsed=json.loads(line)
	text=parsed["text"]
	id=str(parsed["id"]) 
    
	cat=str(int(sheet_train.cell_value(ln,3)))
    
	os.chdir("./"+cat)
	newf = open (id,'w+')

	if text[len(text)-1]=='#':
		text=text[:len(text)-1]
	text=text.replace("\n","")
	text=text.replace("#","")
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
	s=s.strip().lower()

	print (str(cat)+'\t'+str(ln)+'\t'+str(s))

	newf.write(s)
	newf.close()
	os.chdir("../")
	ln+=1

print sheet_train.name
print sheet_test.name