import math, copy
from cmu_112_graphics import *
from tkinter import *
from PIL import Image,ImageTk
import urllib.request
from urllib.request import urlopen
import nltk
import pickle
import ssl
from bs4 import BeautifulSoup
from tkinter import *
import random

#Use conda environment
#Pip install urlopen, bs4, nltk
classifierF = open('naivebayes.pickle', 'rb')
classifier = pickle.load(classifierF)
ssl._create_default_https_context = ssl._create_unverified_context


#All objects
class Movie(object):
    def __init__(self, name, url):
        self.name = name
        self.score = len(name) #initiated by NLP model
        self.url = url
        # resize: self.image2 = self.scaleImage(self.image1, 2/3)
        url = ("https://www.rottentomatoes.com/m/" + self.name.replace(' ', '_') 
               + "/reviews")
        try:
            page = urlopen(url)
        except:
#             print(self.name, 'Bad Url')
            self.score = 0
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
        scores = []
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
        if posScores >= negScores:
            self.score = 1
        elif posScores < negScores:
            self.score = -1

    def getScore(self):
        return self.score

    def getURL(self):
        return self.url

    def getName(self):
        return self.name

def initMovieList(app):
    initMovieList = []
    fullList = [('the dark knight', 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg'), ('despicable me', 'https://m.media-amazon.com/images/M/MV5BMTY3NjY0MTQ0Nl5BMl5BanBnXkFtZTcwMzQ2MTc0Mw@@._V1_.jpg'), ('avengers', 'https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg'), ('suicide squad', 'https://m.media-amazon.com/images/M/MV5BMjM1OTMxNzUyM15BMl5BanBnXkFtZTgwNjYzMTIzOTE@._V1_.jpg'), ('gemini man', 'https://m.media-amazon.com/images/M/MV5BZDJlYzMyZTctYzBiMi00Y2E5LTk4YzgtNzU5YzE0MDZkY2EwXkEyXkFqcGdeQXVyMTA3MTA4Mzgw._V1_FMjpg_UX1000_.jpg'), ('curious george', 'https://m.media-amazon.com/images/M/MV5BODIxNzYxNDEzNl5BMl5BanBnXkFtZTgwMjA1NTM2MTI@._V1_.jpg'), ('a silent voice', 'https://m.media-amazon.com/images/M/MV5BZGRkOGMxYTUtZTBhYS00NzI3LWEzMDQtOWRhMmNjNjJjMzM4XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg'), ('shrek', 'https://m.media-amazon.com/images/M/MV5BOGZhM2FhNTItODAzNi00YjA0LWEyN2UtNjJlYWQzYzU1MDg5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg'), ('shrek the third', 'https://m.media-amazon.com/images/M/MV5BOTgyMjc3ODk2MV5BMl5BanBnXkFtZTcwMjY0MjEzMw@@._V1_FMjpg_UX1000_.jpg'), ('zootopia', 'https://m.media-amazon.com/images/M/MV5BOTMyMjEyNzIzMV5BMl5BanBnXkFtZTgwNzIyNjU0NzE@._V1_FMjpg_UX1000_.jpg'), ('sing', 'https://m.media-amazon.com/images/M/MV5BMTYzODYzODU2Ml5BMl5BanBnXkFtZTgwNTc1MTA2NzE@._V1_.jpg'), ('groundhog day', 'https://m.media-amazon.com/images/M/MV5BZWIxNzM5YzQtY2FmMS00Yjc3LWI1ZjUtNGVjMjMzZTIxZTIxXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg'), ('the last airbender', 'https://m.media-amazon.com/images/M/MV5BMTM1NjE0NDA0MV5BMl5BanBnXkFtZTcwODE4NDg1Mw@@._V1_.jpg'), ('fast and the furious(2009)', 'https://m.media-amazon.com/images/M/MV5BYjQ1ZTMxNzgtZDcxOC00NWY5LTk3ZjAtYzRhMDhlNDZlOWEzXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg'), ('bedtime stories', 'https://m.media-amazon.com/images/M/MV5BMTkwNzc4ODIyOV5BMl5BanBnXkFtZTcwNDY0OTIxMw@@._V1_.jpg'), ('the nightmare before christmas', 'https://m.media-amazon.com/images/M/MV5BNWE4OTNiM2ItMjY4Ni00ZTViLWFiZmEtZGEyNGY2ZmNlMzIyXkEyXkFqcGdeQXVyMDU5NDcxNw@@._V1_FMjpg_UX1000_.jpg'), ('fantastic four', 'https://m.media-amazon.com/images/M/MV5BNWU1ZjFjMTctYjA5ZC00YTBkLTkzZjUtZWEyMjgxY2MxYWM4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg'), ('fantastic mr fox', 'https://m.media-amazon.com/images/M/MV5BOGUwYTU4NGEtNDM4MS00NDRjLTkwNmQtOTkwMWMyMjhmMjdlXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg'), ('jumanji welcome to the jungle', 'https://m.media-amazon.com/images/M/MV5BODQ0NDhjYWItYTMxZi00NTk2LWIzNDEtOWZiYWYxZjc2MTgxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg'), ('alvin and the chipmonks', 'https://m.media-amazon.com/images/M/MV5BMjdmNWY4MjItMjBiMi00MWNiLWI0ZjctYzBjZmEzOGRmNTc5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg'), ('the princess bride', 'https://m.media-amazon.com/images/M/MV5BYzdiOTVjZmQtNjAyNy00YjA2LTk5ZTAtNmJkMGQ5N2RmNjUxXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_FMjpg_UX1000_.jpg'), ('twilight', 'https://m.media-amazon.com/images/M/MV5BMTQ2NzUxMTAxN15BMl5BanBnXkFtZTcwMzEyMTIwMg@@._V1_FMjpg_UX1000_.jpg'), ('thor', 'https://m.media-amazon.com/images/M/MV5BOGE4NzU1YTAtNzA3Mi00ZTA2LTg2YmYtMDJmMThiMjlkYjg2XkEyXkFqcGdeQXVyNTgzMDMzMTg@._V1_FMjpg_UX1000_.jpg'), ('spiderman 2', 'https://m.media-amazon.com/images/M/MV5BMzY2ODk4NmUtOTVmNi00ZTdkLTlmOWYtMmE2OWVhNTU2OTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg'), ('transformers age of extinction', 'https://m.media-amazon.com/images/M/MV5BMjEwNTg1MTA5Nl5BMl5BanBnXkFtZTgwOTg2OTM4MTE@._V1_FMjpg_UX1000_.jpg'), ('your name', 'https://m.media-amazon.com/images/M/MV5BODRmZDVmNzUtZDA4ZC00NjhkLWI2M2UtN2M0ZDIzNDcxYThjL2ltYWdlXkEyXkFqcGdeQXVyNTk0MzMzODA@._V1_FMjpg_UX1000_.jpg'), ('howls moving castle', 'https://m.media-amazon.com/images/M/MV5BMTY1OTg0MjE3MV5BMl5BanBnXkFtZTcwNTUxMTkyMQ@@._V1_FMjpg_UX1000_.jpg'), ('star wars episode i phantom menace', 'https://m.media-amazon.com/images/M/MV5BYTRhNjcwNWQtMGJmMi00NmQyLWE2YzItODVmMTdjNWI0ZDA2XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_FMjpg_UX1000_.jpg'), ('star wars a new hope', 'https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_FMjpg_UX1000_.jpg'), ('indiana jones and the kingdom of the crystal skull', 'https://m.media-amazon.com/images/M/MV5BZmY5ZTk3ZDMtZjA1MS00NzU4LTk5ZDItYmNhOTkxMGYxMjRlXkEyXkFqcGdeQXVyMjM4MzQ4OTQ@._V1_.jpg')]
    indexSet = set()
    for i in range(0,15):
        index = random.randint(0,len(fullList))
        indexSet.add(index)
        while (index in indexSet):
            index = random.randint(0,len(fullList))
        indexSet.add(index)
        initMovieList.append(Movie(fullList[index][0],fullList[index][1]))
    return initMovieList

    
#App

def appStarted(app):
    app.margin = min(app.width//2,app.height//10)
    app.movie = initMovieList(app)
    app.qNo = 0 #qestion No.
    app.score = 0
    url = app.movie[app.qNo].getURL()
    app.image = app.loadImage(url)
    app.imageSize = (app.width//2, app.height//1.5)
    app.timeDelay = 1000
    app.timePass = 0
    app.totalTime = 100000
    app.gain = 0
    app.extraTime=0
    app.currentMovie = app.movie[0]
    image = app.loadImage(app.currentMovie.getURL())
    app.tasteMode = True

# input is main website (https://www.rottentomatoes.com/m/MOVIE_NAME)
def movieImage(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        page = urlopen(url)
    except:
        print( "invalid url")
        return "https://resizing.flixster.com/egbRL1JGgISSrFLb60bv1buHRn0=/300x300/v2/https://flxt.tmsimg.com/assets/161780_bb.jpg"
    html = page.read().decode('unicode_escape')
    strLen = len('''"urls":{"fullscreen":"''')
    imageUrlStart = html.find('''"urls":{"fullscreen":"''') + strLen
    imageUrlEnd = html[imageUrlStart : ].find('"') + imageUrlStart

    res = html[imageUrlStart:imageUrlEnd]#.replace('\u002F', '/')
    # .replace('\u002F', '/')
    return res

def scrapeImage(app):
    app.currentImage = movieImage("https://www.rottentomatoes.com/m/"+ app.movieName)
def createMovie(app):
    window = Tk()
    window.geometry('200x200')
    window.title('Type your moive name!')
    app.text = Text(window, height=10, width=25)
    button = Button(window, height=2, width=20, text='Enter', command=lambda:enterText(app))
    app.text.pack()
    button.pack()
    app.waitInput = True 
def enterText(app):
    app.movieName = app.text.get("1.0", "end-1c")
    newName = ''
    for c in app.movieName.strip():
        if c == ' ':
            newName += '_'
        else:
            newName += c
    app.movieName = newName
    scrapeImage(app)
    app.currentMovie = Movie(app.movieName, app.currentImage)
    app.waitInput = False
    app.image = app.loadImage(app.currentMovie.getURL())

def keyPressed(app, event):
    initial = app.score
    if app.timePass>=app.totalTime+app.extraTime:
        if event.key=="u":
            appStarted(app)
    elif app.qNo<len(app.movie) and app.timePass<app.totalTime+app.extraTime:
        initial = app.score
        if event.key=="Up" or event.key=="Down":
            if event.key=="Up":
                app.score+=app.movie[app.qNo].getScore()
            elif event.key=="Down":
                app.score-=app.movie[app.qNo].getScore()
            app.qNo += 1
            if app.qNo != len(app.movie):
                url = app.movie[app.qNo].getURL()
                app.image = app.loadImage(url)
            if app.score>initial:
                app.gain-=(6*app.timeDelay/app.totalTime)*app.imageSize[1]
                app.extraTime+=6*app.timeDelay
        else:
            print('Invalid')
    else:
        print('Invalid')
    if not app.tasteMode:
        if event.key == 'n':
            createMovie(app)
    if event.key == 'r':
        appStarted(app)
        app.tasteMode = not app.tasteMode


def timerFired(app):
    if app.tasteMode:
        app.timePass+=app.timeDelay
def redrawAll(app, canvas):
    if app.tasteMode:
        sizeY = app.imageSize[1]
        loss = (app.timePass/app.totalTime)*sizeY+app.gain
        if loss>sizeY or app.qNo==len(app.movie):
            canvas.create_text(app.width//2, app.height//2, 
                            text=f"{app.score}",font="Arial 50")
        else:
            canvas.create_text(app.width//2, app.margin, 
                            text=f"Yes/No {app.timePass}")
            canvas.create_text(app.width//8, app.height//2, 
                            text=f"{app.score}",font="Arial 40")
            drawMovie(app, canvas)
            drawLifeline(app, canvas)
            drawQestionScore(app,canvas)
    else:
        drawCustomMovie(app,canvas)
        drawCustomMovieSentiment(app, canvas)

#helper1: page 1 draw selection

def drawMovie(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_text(app.width//2, app.height-app.margin, 
                        text=f"{app.movie[app.qNo].getName()}")
    imageWidth, imageHeight = app.image.size
    desiredWidth, desiredHeight = app.imageSize #desiredImageSize
    ratio = min(desiredWidth/imageWidth,imageHeight/desiredHeight)
    image = app.scaleImage(app.image, ratio)
    canvas.create_image(cx,cy, image=ImageTk.PhotoImage(image))

def drawCustomMovie(app, canvas):
    cx = app.width//2
    cy = app.height//2
    canvas.create_text(app.width//2, app.height-app.margin, 
                        text=f"{app.currentMovie.getName()}")
    imageWidth, imageHeight = app.image.size
    desiredWidth, desiredHeight = app.imageSize #desiredImageSize
    ratio = min(desiredWidth/imageWidth,imageHeight/desiredHeight)
    image = app.scaleImage(app.image, ratio)
    canvas.create_image(cx,cy, image=ImageTk.PhotoImage(image))

def drawCustomMovieSentiment(app, canvas):
    sentiment = ''
    score = app.currentMovie.getScore()
    if score == -1:
        sentiment = 'Negative Critic Sentiment'
    elif score == 1:
        sentiment = 'Positive Critic Sentiment'
    else:
        sentiment = 'Neutral Critic Sentiment'
    canvas.create_text(app.width//2, app.height//10,
                       text=sentiment)

#User Experience
def drawLifeline(app, canvas):
    cx = app.width//8*7
    cy = app.height//2
    sizeX = app.width//16
    sizeY = app.imageSize[1] #height of the poster
    #boarder
    canvas.create_rectangle(cx-sizeX//2,cy-sizeY//2,cx+sizeX//2,cy+sizeY//2, outline="black")
    #lifeline
    loss = (app.timePass/app.totalTime)*sizeY+app.gain
    if loss<0:
        loss=0
    if loss<sizeY:
        if loss<sizeY//2:
            canvas.create_rectangle(cx-sizeX//2,cy-sizeY//2+loss,cx+sizeX//2,cy+sizeY//2, fill="green")
        else:
            canvas.create_rectangle(cx-sizeX//2,cy-sizeY//2+loss,cx+sizeX//2,cy+sizeY//2, fill="red")

def drawQestionScore(app,canvas):
    cx = app.width//8
    cy = app.height*9//10
    score = app.movie[app.qNo].getScore()
    r = app.width//8
    canvas.create_text(cx, app.height*8//10, text="score")
    if score<0:
        canvas.create_text(cx, cy, text=f"{score}", font="Arial 30", fill= "red")
    else:
        canvas.create_text(cx, cy, text=f"{score}", font="Arial 30", fill= "green")
    


runApp(width=400, height=400)
 


    # img= ImageTk.PhotoImage(Image.open("Screen Shot 2565-10-31 at 14.09.27.png"))
