

from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle

#Use conda environment
#Pip install urlopen, bs4, nltk
classifierF = open('naivebayesA.pickle', 'rb')
classifier = pickle.load(classifierF)
ssl._create_default_https_context = ssl._create_unverified_context
def sentReview(movieName):
    newName = ''

    # make input url-friendly
    for c in movieName:
        if c == ' ':
            newName += '_'
        else:
            newName += c
    newName = newName.lower()



    url = ("https://www.rottentomatoes.com/m/" + newName + 
               "/reviews")
    
    # check url validity
    try:
        page = urlopen(url)
    except:
        print('Bad Url')
        return
            
    html = page.read().decode("utf-8")

    reviews = set()
    firstLine = True
    for review in html.split("""<div class="the_review" data-qa="review-text">"""):
        if firstLine == True:
            firstLine = False
            continue

        reviewEnd = review.find("</div>")
        reviews.add(review[ : reviewEnd].strip())

    posSum = 0
    negSum = 0
    neuSum = 0
    sent = SentimentIntensityAnalyzer()
    scores = []
    #From https://nltk-trainer.readthedocs.io/en/latest/train_classifier.html 
    for elem in reviews:
        newElem = elem.split()
        feats = dict([(word, True) for word in newElem])
        newScore = classifier.classify(feats)
        scores.append(newScore)
    negScores = 0
    posScores = 0
    for elem in scores:
        if elem == 'negative':
            negScores += 1
        elif elem == 'positive':
            posScores += 1
    if negScores >= posScores:
        print('Bad Movie')
    elif negScores == posScores:
        print('Neutral Movie')
    else:
        print('Good Movie')
    
    

def main():
    print("Type movies to see their review sentiments. Press 'Q' to quit")
    movieSearch = ''

    while movieSearch != 'Q':
        movieSearch = input("What movie do you want to search?")
        sentReview(movieSearch)

main()
