import wikifetch
from kamrynbot import download_photo
from textToSpeech import textToSpeech
from videoCreator import create_video
import random
import os
import shutil
import time
import re
from instagrapi import Client


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

def seconds_to_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02}:{seconds:02}'


cl = Client()
cl.login("dumbass_bot", "Panchos1472!")


while True:

    try:
        emptyText = True

        while emptyText:
            wikiText = wikifetch.get_paragraph("https://en.wikipedia.org/wiki/Special:Random")
            emptyText = True if wikiText.strip() == "" else False

        wikiText = remove_brackets_content(wikiText)

        randomWords = get_random_words(wikiText,10)

        sortedWords = sorted(randomWords, key=lambda x: x[1])

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

        try:
            cl.clip_upload("output_video.mp4",  wikiText)
            print("Video posted")
        except:
            print("Couldn't post")
    
        folder_path = 'images'

        # Get a list of all files in the folder
        file_list = os.listdir(folder_path)

        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_name}")


        waitTime = random.randint(900,3600)

        for i in range(1,waitTime):
            text = f"Seconds till next post: {seconds_to_time(waitTime-i)}"
            print(text, end='\r', flush=True)
            time.sleep(1)  # Wait for 1 second
    except Exception as e:
        with open("log.txt", "w") as log:
            log.write(str(e))
        os.system('shutdown /s /f /t 10')