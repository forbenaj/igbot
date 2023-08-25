from bs4 import BeautifulSoup
import urllib.request as request
from random import randint
from PIL import Image
import time

def create_photo():
    #define the search terms
    search = ["tomato", "lime", "rave", "nightmare", "juice",
    "wallet", "summer", "sun", "fun", "extreme",
    "skating", "blister", "turntable", "download", "john",
    "presentation", "i+hate", "large+item", "support", "culture",
    "social", "bricks", "funky", "demonic", "satanic",
    "christian", "coke", "product", "productivity", "electronic",
    "techno", "genius", "window", "sport+ball", "fabric+softener",
    "dog+white+background", "tree+white+background", "cheese+can", "yo+dawg", "bitchhh",
    "dub", "iPhone+Help+Me", "Ad", "Advertisement", "Potato",
    "wow+awesome", "super+cool+text", "dorito+eating", "drinking", "funny",
    "great+joke", "jokester", "prank+white+background", "nike+commercial", "whale+white+background",
    "OMG+becky", "oh+god", "walmart+hair", "walmart+funny", "funny+great+joke",
    "insane", "crazy", "astonishing+text", "bald", "3d+shapes",
    "array", "clean", "dazzling", "drab", "stun+gun",
    "fancy+text", "fit", "fat+loss", "that+sucks", "dvi",
    "ewww", "scary", "upright", "worried+clip+art", "tiny+clip+art",
    "single+board", "teenage+drama", "teen+culture+comic", "big", "starch",
    "fat", "gamer", "funny+cheese", "george", "milk",
    "puny", "partial", "clean+cut",  "yacht", "dis",
    "man", "dad", "spatula", "bogus", "fight",
    "warfare+crazy+and+cool", "battlefield", "free+download", "download+now", "download",
    "intranet", "bitcoin", "current+event", "stockmarket", "fighting+for+freedom",
    "we+deserve+better", "internet+explorer+interface", "finding+it", "searching+clipart", "join",
    "interesting+facts", "new+keyboard", "open+source", "apache+license", "yahoo+questions",
    "more+information+needed", "fact+driven", "fork", "one+metric+tonne", "elephant+chart",
    "super+mario+character", "evolution", "really+dry+cartoon", "video+game+character", "newspaper+graphic",
    "celebrity+beef", "pop+music", "earth+core", "melodic+death+metal", "oregon",
    "peace", "super", "paint+can", "trash", "powerpoint+background",
    "free+powerpoint+backgrounds", "coolest+thing+ever", "microsoft+product", "serious", "real+life",
    "family+guy+season+2+episode+6", "10+minutes", "oh+please", "dont+do+it", "iphone+unboxing",
    "whats+up", "arrgh", "hello+kitty", "food+addiction", "krusty+krab",
    "dental", "i+guess", "i+would+like+to+say+thanks+to+all+my+fans+out+there+i+couldnt+do+it+without+you+guys",
    "real+hell", "are", "51", "30", "blocks", "I+Listen+To+Metal", "5+reasons",
    "top+10", "free+giveaway"]

    #select a random word
    randomWord = search[randint(0,len(search)-1)]

    #search the selected word
    url = 'https://images.search.yahoo.com/search/images?p=' + randomWord

    print(url)

    #grab the html of the search result page
    page = request.urlopen(url)
    htmlData = BeautifulSoup(page, 'html.parser')

    #find search result images within the html and download a random one
    randomResult = randint(0,30)
    count = 0
    for image in htmlData.find_all('img', class_=""):
        imgLink = image.get('src')
        if count == randomResult:
            imageFile = open(f'images/{randomWord}.jpg', 'wb')
            imageFile.write(request.urlopen(imgLink).read())
            imageFile.close()
            print(f'{randomWord}.jpg downloaded')
            break
        count += 1


    

    #enlarge the small image
    imageFile = Image.open(f'images/{randomWord}.jpg')
    bigSize = (256, 256)
    bigImage = imageFile.resize(bigSize, Image.BILINEAR)
    bigImage.save(f'images/{randomWord}.jpg')
    print(f'{randomWord}.jpg edited')


if __name__ == "__main__":
    create_photo()
    create_photo()
    create_photo()
    create_photo()
    create_photo()