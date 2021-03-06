# -*- coding: utf-8 -*-
"""Programming Assignment 4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LbKMZYnZLdIjbJNxfuf1MnxfnX95HSqt
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import collections
from collections import Counter
from scipy.special import expit
import string

!gdown --id 1n0j5zbMXMVnLPUqadFNcCxiZRu0ChoXL
!unzip -q "Programming_Assignment_3.zip" -d ""

test = pd.DataFrame()
train = pd.DataFrame()
label_list = []
content = []

def file_reading(datatype,directory):
#   files = glob.glob('Dataset/'+datatype+'/'+directory+'/*.txt',  recursive = True)
    files = glob.glob('Dataset/'+datatype+'/'+directory+'/*.txt',  recursive = True)

    print("Files are :",len(files))
  # return
    if directory == 'neg':
        label = 0
    else:
        label = 1

    print("Sentiment is: ",label)
    for file in files:
        f = open(file,'r')
        content.append(f.read())
        label_list.append(label)
    # print('Content:  ',content[0])

file_reading('test','neg')
file_reading('test','pos')

test['Review'] = content
test['Label'] = label_list

label_list = []
content = []
file_reading('train','neg')
file_reading('train','pos')
train['Review'] = content
train['Label'] = label_list

def preprocessing(data):
  f = open('Dataset/stop_words.txt','r')
  stop_words = f.read()
  punctuation = string.punctuation

  data['Review'] = data['Review'].str.replace('<br />',' ')
  data['Review'] = data['Review'].str.replace('[^\w\s*-]',' ')
  data['Review'] = data['Review'].str.replace('[\d]',' ')
  data['Review'] = data['Review'].str.lower()
  data['without_stopwords'] = data['Review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
  data['Review'] = data['without_stopwords']
  data.drop(columns='without_stopwords',inplace = True)
  
  return data

train = preprocessing(train)
test = preprocessing(test)

train.head()

"""# Part 1"""

type(train['Label'][0])

def unique_words(D):
  unique_list = set()
  list_words = D.str.split()
  list_words.apply(unique_list.update)
  unique_list = list(unique_list)

  return unique_list, len(unique_list)

def vocab(D):
  count = 0
  total_vocab = []
  list_words = D.str.split()
  for i in list_words:
    count = count + len(i)
    for w in i:
      total_vocab.append(w)
  # print(list_words)
  return count,total_vocab

# cnt, list_v = vocab(train['Review'])
# list_v[:5]
len(train[train['Label']==0]['Review'])
uniq_ls,cnt = (unique_words(train['Review']))
len(uniq_ls)

# unique_words(train['Review'])
# cnt

# unique_list = set()
# list_words = train['Review'].str.split()
# list_words.apply(unique_list.update)
# unique_list = list(unique_list)
# len(unique_list)

def alt_denomenator(V,list_of_words):
  print('Calculating denomenator for likelihood! (using alt method)')
  total = len(list_of_words)
  unique_words = len(V)

  count = total+unique_words
  return count

def denominator(V,list_of_words):
  print('Calculating denomenator for likelihood!')
  print(list_of_words[0:5])
  print('number of words in V: ',len(V))
  count = 0
  for word in V:
    word_cnt = list_of_words.count(word)
    count = count + (word_cnt + 1)
  return count

def train_NB(D,C):
  print(D['Review'].head())
  count = {}
  loglikelihood = {}
  logprior = np.zeros(len(C))
  bigdoc = {}
  for class_i in C:
    print("Running for class ",class_i)
    N_doc = len(D['Review'])
    N_class = len(D[D['Label']==class_i]['Review'])
    logprior[int(class_i)] = np.log(N_class / N_doc)
    V , cntV= unique_words(D['Review'])
    _, bigdoc[int(class_i)] = vocab(D[D['Label']==class_i]['Review'])
    # sampled_denom = denominator(V,bigdoc[class_i])
    sampled_denom2 = alt_denomenator(V,bigdoc[class_i])
    # print('Value of denom ',sampled_denom)
    print('Value of denom 2 ',sampled_denom2)
    # return 0
    print('Calculating Log liklihood Next')
    word_cnt = Counter(bigdoc[class_i])
    for word in V:
      if word in word_cnt.keys():
        count[(word,class_i)] = word_cnt[word]
      else:
        count[(word,class_i)] = 0
      # sampled_denom = alt_denomenator(V,bigdoc[class_i])
      # print('Value of denom ',sampled_denom)
      # count[(word,class_i)] = bigdoc[class_i].count(word)
      # if count == 0:
      #   print(word)
      loglikelihood[(word,class_i)] = np.log((count[(word,class_i)] + 1) / sampled_denom2)
      # print(loglikelihood)
  
  return logprior,loglikelihood,V

C = list(set(train['Label']))
C

# train_NB(train,C)

logprior,loglikelihood,V = train_NB(train,C)

# loglikelihood[('resignation',0)]

# np.log(0.5)

def test_NB(testdoc,logprior,loglikelihood,C,V):
  sum = np.zeros(len(C))
  set_V = set(V)
  # print(len(V),len(set_V))
  # return 0
  for class_i in C:
    sum[class_i] = logprior[class_i]
    for i in testdoc.split():
      word = i
      # print(word)
      # return 0
      if word in set_V:
        sum[class_i] = sum[class_i]+ loglikelihood[(word,class_i)]
  return np.argmax(sum)

# lbl = test_NB(test['Review'][i],logprior,loglikelihood,C,V)
# lbl

predicted_lbls = []
for i in range(len(test['Review'])):
  lbl = test_NB(test['Review'][i],logprior,loglikelihood,C,V)
  predicted_lbls.append(lbl)
  # if i % 1000 ==0:
  #   print('Running ', i)  
  # if i == 100:
  #   # print('Running')
  #   break

test['Predicted'] = predicted_lbls
test.head()

def classification_accuracy(actual, predicted):
    total = len(actual)
    correct = 0
    for i in range(total):
        if actual[i] == predicted[i]:
            correct = correct + 1
  # query = np.where(actual == predicted,1,0)
  # occurrence_counts = Counter(query)
  # correct = occurrence_counts[1]
    accuracy = (correct/total) * 100

    return accuracy

print('Accuracy of the model is: ',classification_accuracy(test['Label'],test['Predicted']),'%')

"""# Part 2"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

vectorizer = CountVectorizer()
train_X = vectorizer.fit_transform(train['Review'])
train_y = train['Label']

test_X = vectorizer.transform(test['Review'])
test_y = train['Label']

clf = MultinomialNB()
clf.fit(train_X, train_y)

y_predicted = clf.predict(test_X)
print("The accuracy is : ",accuracy_score(test_y, y_predicted))
print('Confusion Matrix:\n',confusion_matrix(test_y, y_predicted))

