from bs4 import BeautifulSoup
import urllib.request as request
from urllib.parse import quote
from random import randint
import re
from PIL import Image


def download_photo(word,number):
    
    filename = re.sub(r'[<>:"/\\|?*]', '_', word+str(number))


    #search the selected word
    url = 'https://images.search.yahoo.com/search/images?p=' + quote(word,safe='')

    #grab the html of the search result page
    page = request.urlopen(url)
    htmlData = BeautifulSoup(page, 'html.parser')

    #find search result images within the html and download a random one
    randomResult = randint(0,30)
    count = 0
    for image in htmlData.find_all('img', class_=""):
        imgLink = image.get('src')
        if count == randomResult:
            imageFile = open(f'images/{filename}.jpg', 'wb')
            imageFile.write(request.urlopen(imgLink).read())
            imageFile.close()
            break
        count += 1


    

    # Change image size
    try:
        imageFile = Image.open(f'images/{filename}.jpg')
        print(f'"{word}.jpg" downloaded')
    except FileNotFoundError:
        imageFile = Image.open('missing-file.jpg')
        print(f'Couldn\'t download "{word}.jpg" ')
    bigSize = (256, 256)
    bigImage = imageFile.resize(bigSize, Image.BILINEAR)
    bigImage.save(f'images/{filename}.jpg')
    


if __name__ == "__main__":
    download_photo("damn+content+harvest",1)