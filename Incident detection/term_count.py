import json
import tweepy
import os
from data_helpers import clean_str
from nltk import *
import operator

CONSUMER_KEY='aY3uy6TAPp718hli4D1K8YzMD'
CONSUMER_SECRET='OvT98IPs4HB8BuFZHbWZVOH2ljNvA5fgiscjtTRtxgCN7neNBT'
OAUTH_TOKEN='843013273855365124-MIm4RYEK7uUdwIenqa0q6kWQE7eKMlF'
OAUTH_TOKEN_SECRET='BmBUWXS3PtCClWkzb4pLVhq77ttf2xUTefcBLj5FDDloM'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

stemmer= PorterStemmer()

with open('train.json') as f:
    data = json.load(f)
f.close()

os.chdir("./tweet_ids/")
events=os.listdir(".")
events.sort()
os.chdir("../")

os.chdir ("./train/")

for i in range (1,2):
	os.chdir ("./{}/".format(events[i]))
	file_list=os.listdir(".")
	tweet_list=data["events"][i]["tweets"]

	categories=dict()
	handle=dict()
	for tweet in tweet_list:
		categories[tweet["categories"][0]]={}
		handle[tweet["categories"][0]]={}
	for tweet in tweet_list:
		if tweet["postID"] not in file_list:
			continue	
		cat=tweet["categories"][0]
		tf=open(tweet["postID"],'r')
		for l in tf:
			if l[-1]=='\n':
				l=l[:-1]
			if (len(l)==0):
				continue
			wl=l.split()
			for w in wl:
				ws=stemmer.stem(w)
				if ws in categories[cat].keys():
					categories[cat][ws]+=1
				else:
					categories[cat][ws]=1

	for cat in categories.keys():
		temp_dict=categories[cat]
		sorted_temp_dict=sorted(temp_dict.items(), key=operator.itemgetter(1))[::-1]
		print "{} :   {}".format(cat,sorted_temp_dict)
		print
		print



