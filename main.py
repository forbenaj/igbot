import wikifetch
from kamrynbot import download_photo
from textToSpeech import textToSpeech
from videoCreator import create_video
import random

def get_random_words(sentence, num_words):
    words = sentence.split()
    long_words = [(word, index) for index, word in enumerate(words) if len(word) > 4]
    
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


wikiText = wikifetch.get_paragraph("https://en.wikipedia.org/wiki/Special:Random")

wikiText = remove_brackets_content(wikiText)

randomWords = get_random_words(wikiText,10)

sortedWords = sorted(randomWords, key=lambda x: x[1])

print(sortedWords)

fileNames = []
durations = []

last = 0
for word in sortedWords:
    download_photo(word[0],word[1])
    fileNames.append(f"images/{word[0]}{word[1]}.jpg")
    durations.append((word[1]-last)/2)
    last = word[1]

durations.pop(0)

durations.append((len(wikiText.split())-last)/2)

textToSpeech(wikiText)

print(fileNames,durations)

create_video(fileNames,durations)