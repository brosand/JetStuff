#going onto video 5-6 https://www.youtube.com/watch?v=7fcWfUavO7E

'''
to create lexicon
[chair, table, spoon, television]
I pulled the chair up to the table
np.zeros(len(lexicon))
[0 0 0 0]
[1 0 0 0]
[1 1 0 0]
'''

#PREPROCESSING

import nltk
from nltk.tokenize import word_tokenize
#separates the sentence into words

from nltk.stem import WordNetLemmatizer
#run, running, ran all the same 
#lots of preprocessing

import numpy as np
import random
import pickle
from collections import Counter

lemmatizer = WordNetLemmatizer()
hm_lines = 10000000

def create_lexicon(pos, neg):
    lexicon = []
    #here we've populated the lexicon with every word that we have come across
    for fi in [pos, neg]:
        with open(fi, 'r') as f: #so you can read
            contents = f.readlines()
            for l in contents[:hm_lines]:
                all_words = word_tokenize(l.lower)
                lexicon += list(all_words)

    #lemmatize everything
    lexicon = [lemmatizer.lemmatize(i) for i in lexicon]
    #count words
    w_counts = Counter(lexicon)
    #here's what that dictionary looks like: w_counts = {'the':52521, 'and':25242}
    #l2 is the final lexicon
    l2 = []
    for w in w_counts:
        #don't want too common words
        if 1000 > w_counts[w] > 50:
            l2.append(w)
    print(len(l2))
    return l2

def sample_handling(sampling, lexicon, classification)
    featureset = []

'''what is a featureset?
a list of lists
[
[[0 1 0 1 1 0], [1, 0]] //second part is the positive or negative

]
'''

    with open(sample, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            current_words = word_tokenize(l.lower)
            current_words = [lemmatizer.lemmatize(i) for i in current_words]
            features = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    index_value = lexicon.index(word.lower())
                    features[index_value] += 1
            features = list(features)
            featureset.append([features, classification])

    return featureset

def create_feature_sets_and_labels(pos, neg, test_size=0.1):
    lexicon = create_lexicon(pos,neg)
    features = []
    features += sample_handling('pos.txt', lexicon, [1,0])
    features += sample_handling('neg.txt', lexicon, [0,1])
    random.shuffle(features) #v imp to shuffle

    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,1][:-testing_size])

''' what does :,0 do?
say you have a list of arrays
[[5,8], 
[7,9]]

:,0 says give me all the 0th elements, so [5,7]

so in this case...
[[features, label],
[features, label],
[features, label]
]

but each features is an array [0 1 1 0 1]
'''

    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,0][-testing_size:])

    return train_x, train_y, test_x, test_y

if __name__ == '__main__':
    train_x, train_y, test_x, test_y = create_feature_sets_and_labels('pos.txt', 'neg.txt')
    with open('sentiment_set.pickle', 'wb') as f:
        pickle.dump([train_x, train_y, test_x, test_y], f)





            



