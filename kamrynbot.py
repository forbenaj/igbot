from bs4 import BeautifulSoup
import urllib.request as request
from random import randint
from PIL import Image


def download_photo(word,number):
    #define the search terms


    #search the selected word
    url = 'https://images.search.yahoo.com/search/images?p=' + word

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
            imageFile = open(f'images/{word}{number}.jpg', 'wb')
            imageFile.write(request.urlopen(imgLink).read())
            imageFile.close()
            print(f'image "{word}" downloaded')
            break
        count += 1


    

    #enlarge the small image
    imageFile = Image.open(f'images/{word}{number}.jpg')
    bigSize = (256, 256)
    bigImage = imageFile.resize(bigSize, Image.BILINEAR)
    bigImage.save(f'images/{word}{number}.jpg')
    print(f'image "{word}" edited')


if __name__ == "__main__":
    download_photo("image",1)