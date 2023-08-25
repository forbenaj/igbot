from gtts import gTTS

# Text to be converted to speech
text = "Hello, this is a sample text to be converted to speech."

# Language in which you want to convert
language = 'en'  # English

# Passing the text and language to the engine
tts = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a file
tts.save("output.mp3")