import os
import math
import pickle
from sklearn import svm
import matplotlib.pyplot as plt 
import nltk
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.datasets import make_classification

def form_features (max_len, exclude, cwise, idf, entropy, stoplist, k):

    stemmer = nltk.PorterStemmer()

    features = []
    labels = []
    sentences = []
    for cls in range(9):
        thiscls=[]
        os.chdir("./"+str(cls))
        fl_temp=os.listdir(".")
        fl = [name for name in fl_temp if name not in exclude]
        for name in fl:
            sentence=[]
            f=open(name,'r')
            for l in f:
                line = l.strip()
                for word in line.split():
                    if word not in stoplist and len(word)>2 and word[0] not in ['0','1','2','3','4','5','6','7','8','9','\'',"\"",'/','\\','.',',',';','!',':']:
                        #w_stem = stemmer.stem(word)
                        w_stem=word
                        sentence.append(w_stem)
            f.close()

            padding_word="<PAD/>"
            num_padding = max_len - len(sentence)
            new_sentence = sentence + [padding_word] * num_padding
            thiscls.append(new_sentence)
        sentences.append(thiscls)
        os.chdir("../")
    train_vocab = idf.keys()

    for cln in range(9):
        kc= len(cwise[cln].keys())
        for sentence in sentences[cln]:
            vector =[]
            for word in sentence:
                if word not in train_vocab:
                    vector.append(0.0)
                    continue
                value = (float(sentence.count(word))*float(idf[word]))/float(len(sentence))
                iw = 0.0
                if word in cwise[cln].keys():
                    iw=float(cwise[cln][word])
                    iw/=float(kc)
                value = value + (float(entropy[word])*float(iw))/float(k)
                vector.append(value)
            features.append(vector)
            labels.append(cln)
    

    return features, labels

incident = "earthquake"
n=6007

max_len = 40

os.chdir("./"+incident+"_train")

f_cwise = open ("cwise", "rb")
f_idf = open ("idf", "rb")
f_entropy = open ("entropy", "rb")

cwise = pickle.load(f_cwise)
idf = pickle.load(f_idf)
entropy = pickle.load(f_entropy)

f_cwise.close()
f_idf.close()
f_entropy.close()

stoplist=[]
fstop=open('../stopwords','r')
for l in fstop:
    if l[0]!='\n':
        l=l[:-1]
        stoplist.append(l)
fstop.close()

val_k=[]
accuracy = []

os.chdir("../")

#for k in [1,2,3,4,5,6,7,8,9,10]:
for k in [1e-13,1e-12,1e-11,1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10 , 100 , 1000, 10000, 100000, 1000000]:
#for k in [1e4,1e5,1e6,1e7,1e8,1e9,1e10,1e11,1e12,1e13,1e14,1e15,1e16]:
    kt=float(k)#*float(1e-11)

    os.chdir("./"+incident+"_train")
    exclude = []
    f_ex = open("../Media Train/"+incident+".jsonmedia")
    for l in f_ex:
        line = l.strip()
        exclude.append(str(line))
    f_ex.close()
    train_features,  train_labels = form_features (max_len, exclude, cwise, idf, entropy, stoplist,kt)


    smote = SMOTE('all')
    #smote = SMOTE('not minority')
    train_features , train_labels = smote.fit_sample(train_features, train_labels)

    print len(train_labels)

    os.chdir("../"+incident+"_test")
    exclude = []
    f_ex = open("../Media Test/"+incident+".jsonmedia")
    for l in f_ex:
        line = l.strip()
        exclude.append(str(line))
    f_ex.close()
    test_features,  test_labels = form_features (max_len, exclude, cwise, idf, entropy, stoplist,kt)

    #clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
    #clf = svm.LinearSVC(random_state=0, tol=1e-5)
    #clf = RandomForestClassifier(n_estimators=100)
    clf = BaggingClassifier(n_estimators = 100)
    clf.fit (train_features, train_labels)

    svm_test = clf.score(test_features, test_labels)
    val_k.append(kt)
    accuracy.append(svm_test)
    print kt,svm_test

    os.chdir("../")

plt.plot(val_k, accuracy) 

plt.xlabel('k') 
plt.ylabel('accuracy') 
 
plt.title('My first graph!') 

plt.show() 
