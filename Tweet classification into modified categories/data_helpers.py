import numpy as np
import re
import itertools
from collections import Counter
from nltk import *
import os

"""
Original taken from https://github.com/dennybritz/cnn-text-classification-tf
"""
lemmatizer = WordNetLemmatizer()
stemmer= PorterStemmer()


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels():
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    positive_examples = []
    negative_examples = []

    # Load data from files
    os.chdir ("./dev/")
    fldev=os.listdir(os.getcwd())
    fldev.sort()
    for fn in fldev:
        f=open(fn,'r')
        for l in f:
            positive_examples.append(l)

    #empty=[623, 1347, 3903, 4155, 5951, 7175, 8227, 10287, 10461, 11670, 12056, 12270, 12421, 13030, 13186, 13237, 13383, 15267, 15749, 17585, 18044, 18261, 18550, 18893, 19348, 19419, 19446, 19655, 19694, 20201, 20256, 20605, 20879, 22931, 23049, 23145, 23738, 24639, 24755, 25691, 25697, 25802, 25804, 25824, 26528, 26704, 27552, 27720, 27755, 28496, 29849, 30984, 31260, 31333, 31523, 32500, 35698, 35951, 37201, 37433, 37478, 38126, 38657, 38675, 38682, 39955, 40226, 41929, 42289, 42751, 43047, 43609, 44553, 44766, 44840, 45427, 46422, 46484, 48901, 49550]
    raw_test=[]
    os.chdir ("../test/")
    fltest=os.listdir(os.getcwd())
    fltest.sort()
    for fn in fltest:
        f=open(fn,'r')
        for l in f:
            negative_examples.append(l)
        raw_test.append((fn,l))

    os.chdir("../")

    # Split by words
    #fe=open("empty",'a+')
    #for i in empty:
    #    fe.write(str(negative_examples[i])+'\n')
    #fe.close()
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    x_text = [s.split() for s in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)

    return [x_text, y,raw_test]


def pad_sentences(sentences, padding_word="<PAD/>"):
    """
    Pads all sentences to the same length. The length is defined by the longest sentence.
    Returns padded sentences.
    """
    sequence_length = max(len(x) for x in sentences)
    print "The sequence length is "+str(sequence_length)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences,sequence_length


def build_vocab(sentences):
    """
    Builds a vocabulary mapping from word to index based on the sentences.
    Returns vocabulary mapping and inverse vocabulary mapping.
    """
    # Build vocabulary
    word_counts = Counter(itertools.chain(*sentences))
    # Mapping from index to word
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    # Mapping from word to index
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]


def build_input_data(sentences, labels, vocabulary):
    """
    Maps sentencs and labels to vectors based on a vocabulary.
    """
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    y = np.array(labels)
    return [x, y]

def stopword(sentences):
    new_sentences=[]
    stoplist=[]
    fstop=open('stopwords','r')
    for l in fstop:
        if l[0]!='\n':
            l=l[:-1]
            stoplist.append(l)
    fstop.close()
    for sent in sentences:
        temp=[]
        for w in sent:
            fl=0
            for x in w:
                if  x not in ['0','1','2','3','4','5','6','7','8','9']:
                    fl=1
                    break
            if fl and w!=" " and (stemmer.stem(w)[0] not in ['\\',"\'",'\"']):
                if (w not in [',','.',"\'","\"",'nepal','earthquake','quake']+stoplist):
                    temp.append(str(stemmer.stem(w)))
        new_sentences.append(temp)
    return new_sentences

def stopword_2(sentences):
    new_sentences=[]
    stoplist=[]
    fstop=open('stopwords','r')
    for l in fstop:
        if l[0]!='\n':
            l=l[:-1]
            stoplist.append(l)
    fstop.close()
    for sent in sentences:
        temp=[]
        for w in sent:
            if w!=" " and (stemmer.stem(w)[0] not in ['\\',"\'",'\"']):
                if (w not in [',','.',"\'","\"",'nepal','earthquake','quake']+stoplist):
                    temp.append(str(stemmer.stem(w)))
        new_sentences.append(temp)
    return new_sentences

def load_data():
    """
    Loads and preprocessed data for the MR dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    stoplist=[]
    fstop=open('stopwords','r')
    for l in fstop:
        if l[0]!='\n':
            l=l[:-1]
            stoplist.append(l)
    fstop.close()
    print stoplist
    sentences, labels,raw_test, = load_data_and_labels()
    sentences=stopword(sentences)
    sentences_padded, sequence_length = pad_sentences(sentences)
    print (len(sentences_padded[1]))
#    for i in  range (20):
#        print sentences_padded[i]
    vocabulary, vocabulary_inv = build_vocab(sentences_padded)
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv, sequence_length,sentences,raw_test]


def batch_iter(data, batch_size, num_epochs):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data) / batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_data = data[shuffle_indices]
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
