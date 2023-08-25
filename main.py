import wikifetch
from kamrynbot import download_photo
from textToSpeech import textToSpeech
from videoCreator import create_video
from instabot import Bot
import random
import os
import shutil
import time
import re

def get_random_words(sentence, num_words):
    words = sentence.split()
    long_words = [(word, index) for index, word in enumerate(words) if len(word) > 3]
    
    if num_words >= len(long_words):
        return long_words
    
    random_words = random.sample(long_words, num_words)
    random_words.append((f"{words[0]}+{words[1]}",1))
    return random_words

def remove_brackets_content(text):
    while '[' in text and ']' in text:
        start = text.index('[')
        end = text.index(']')
        text = text[:start] + text[end + 1:]
    return text


# Create a Bot instance
bot = Bot()

# Login to your Instagram account
bot.login(username="daily_content_harvest", password="panchos")


while True:


    emptyText = True

    while emptyText:
        wikiText = wikifetch.get_paragraph("https://en.wikipedia.org/wiki/Special:Random")
        emptyText = True if wikiText.strip() == "" else False

    wikiText = remove_brackets_content(wikiText)

    randomWords = get_random_words(wikiText,10)

    sortedWords = sorted(randomWords, key=lambda x: x[1])

    print(sortedWords)

    fileNames = []
    durations = []

    last = 0
    for word in sortedWords:
        filename = re.sub(r'[<>:"/\\|?*]', '_', word[0]+str(word[1]))
        download_photo(word[0],word[1])
        fileNames.append(f"images/{filename}.jpg")
        durations.append((word[1]-last)/2)
        last = word[1]

    durations.pop(0)

    durations.append((len(wikiText.split())-last)/2.3)

    textToSpeech(wikiText)

    print(fileNames,durations)

    create_video(fileNames,durations)


    bot.upload_video("output_video.mp4", caption=wikiText)

   
    folder_path = 'images'

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_name}")

    try:
        shutil.rmtree("config")
    except FileNotFoundError:
        pass
    except PermissionError:
        print("Permission Error")
    time.sleep(500)