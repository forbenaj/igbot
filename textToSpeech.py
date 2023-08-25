from gtts import gTTS

def textToSpeech(text):
    # Text to be converted to speech

    # Language in which you want to convert
    language = 'en'  # English

    # Passing the text and language to the engine
    tts = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a file
    tts.save("output.mp3")

if __name__ == "__main__":
    textToSpeech("This is a test text")