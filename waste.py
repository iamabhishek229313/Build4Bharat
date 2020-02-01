def toSpeech(text):
    myObj = gTTS(text=text , lang = language,slow=False)
    temp = BytesIO()
    myObj.write_to_fp(temp)
    temp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(temp)
    pygame.mixer.music.play()