from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

#Use conda environment
#Pip install urlopen, bs4, nltk
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
    scores = dict()
    for elem in reviews:
        scores[elem] = (sent.polarity_scores(elem))
    for elem in scores:
        posSum += scores[elem]['pos']
        negSum += scores[elem]['neg']
        neuSum += scores[elem]['neu']
    numReviews = len(reviews)
    if numReviews != 0:
        goodUrl = True
    posMean = posSum/numReviews
    negMean = negSum/numReviews
    neuMean = neuSum/numReviews
    print('Pos Mean is', posMean, 'Neg Mean is', negMean, 'Neu Mean is', neuMean)
    if negMean > posMean:
        return('Bad Movie')
    if posMean > negMean:
        return('Good Movie')

def main():
    print("Type movies to see their review sentiments. Press 'Q' to quit")
    movieSearch = ''

    while movieSearch != 'Q':
        movieSearch = input("What movie do you want to search?")
        sentReview(movieSearch)

main()
