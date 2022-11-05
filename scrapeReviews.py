from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.rottentomatoes.com/m/black_adam/reviews"
page = urlopen(url)

html = page.read().decode("utf-8")

reviews = set()
firstLine = True
for review in html.split("""<div class="the_review" data-qa="review-text">"""):
    if firstLine == True:
        firstLine = False
        continue

    reviewEnd = review.find("</div>")
    reviews.add(review[ : reviewEnd].strip())

for elem in reviews:
    print(elem)
    print()