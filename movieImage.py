from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup


# input is main website (https://www.rottentomatoes.com/m/MOVIE_NAME)
def movieImage(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        page = urlopen(url)
    except:
        print( "invalid url")
    html = page.read().decode('unicode_escape')
    strLen = len('''"urls":{"fullscreen":"''')
    imageUrlStart = html.find('''"urls":{"fullscreen":"''') + strLen
    imageUrlEnd = html[imageUrlStart : ].find('"') + imageUrlStart

    res = html[imageUrlStart:imageUrlEnd]#.replace('\u002F', '/')
    # .replace('\u002F', '/')
    return res

# test
url = "https://www.rottentomatoes.com/m/up"
page = urlopen(url)
print(movieImage(url))