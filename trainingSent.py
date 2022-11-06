import nltk
import random
import pickle 
import csv
import tqdm
from nltk.corpus import stopwords
#Paraphrased from https://pythonprogramming.net/pickle-classifier-save-nltk-tutorial/
filename = "dataset.csv"
stopWords = set(stopwords.words('english'))
with open(filename, mode='r',encoding='utf-8') as f:
    file = csv.reader(f)
    newFile = []
    for line in file:
        newFile.append((line[0].lower().split(), line[1]))
# print(newFile)
random.shuffle(newFile)
                                              
allWords = []
for i in range(len(newFile)):
    for word in newFile[i][0]:
        if word not in stopWords:
            allWords.append(word)

allWords = nltk.FreqDist(allWords)
lenAllWords = len(allWords)
wordFeatures = list(allWords.keys())[:8000]

def findFeatures(document):
    words = set(document)
    features = {}
    for w in wordFeatures:
        features[w] = (w in words)
    print('t')
    return features
featureSet = []
for line in newFile:
    featureSet.append(((findFeatures(line[0]), line[1])))
    # print((findFeatures(line[0]), line[1]))
trainingSet = featureSet[len(featureSet)//2:]
testSet = featureSet[:lenAllWords//2]
tests = 1
bestModel = None
bestAcc = 0.0
for i in tqdm.tqdm(range(tests)):
    classifier = nltk.NaiveBayesClassifier.train(trainingSet)
    accuracy = (nltk.classify.accuracy(classifier, testSet))*100
    if i == 0:
        bestModel = classifier
        bestAcc = accuracy
    else:
        if accuracy > bestAcc:
            bestModel = classifier
            bestAcc = accuracy
classifier = bestModel
print(bestAcc)
saveClassifier = open('naivebayes.pickle', 'wb')
pickle.dump(classifier, saveClassifier)
saveClassifier.close()
classifier.show_most_informative_features(15)
classifierF = open('naivebayes.pickle', 'rb')
classifier = pickle.load(classifierF)
classifierF.close()
