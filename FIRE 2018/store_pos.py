from data_helpers import *
f=open("output",'r')
for l in f:
    l=l[:-1]
    id=l.split('\t')[1]
    tweet=l.split('\t')[2]
    tweet=clean_str(tweet)
    tokens=tweet.split()
    stop_tokens=stopword_2([tokens])[0]
    tweet=' '.join(stop_tokens)
#    print "{} {}".format(id,tweet)
    os.chdir('./positive/')
    fout=open(str(id),'w+')
    if tweet[-1] in ['.',',',';','!','/','\\',"\'",'\"']:
        print "Found "+tweet[-1]
        tweet=tweet[:-1]
    fout.write(tweet)
    fout.close()
    os.chdir("../")

    