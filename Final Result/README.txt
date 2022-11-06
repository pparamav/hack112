Hello! Welcome to our program!
Before you get started if you want to use it yourself, you'll need a couple things:
First, pip install these packeges:
nltk
ssl
urlopen
bs4
pickle

And make sure to have the pickle file(the classifier model) in the same folder as the script and cmu_112_graphics.

Second, create a new conda environment

And third, cd to the script's directory and run the script in the environment.

How to use:
When the app initially loads up, it begins in taste-rating mode!
Press up if you think the movie is good
Press down if you think it isn't 
You will gain/loose score depending on whether the model says the critical sentiment agrees with you

If you restart the app and press 'r', you're put into lookup mode:
Press 'n' to open up an entry box
type in the movie you want to look up and click the enter button on the window
Voila! The moive and the sentiment appears in the app
If the name is incorrect, a picture of the grinch will show instead. 

Restart the app to go back to taste-rating mode

How it was made:
Our app uses a combination of web-scraping, natural language processing, and machine learning to produce our result.
Using beautiful soup, we scrape both the image and the critic reviews off of Rotten Tomatoes for each movie
Then, the language is parsed using natural language toolkit, and fed into our classifying model
The model, using the naivebayes and supervised learning for training was trained off of a dataset of 50,000 labeled movie reviews from IMDB
Finally, the model outputs whether the average sentiment was positive or negative for each movie.

Included are two different models, one trained with more parameters, and the other trained for longer. Each model had a reported 80% accuracy in its prediction

Here is the link to our github repository: https://github.com/pparamav/hack112

Thank you and enjoy!
