from gtts import gTTS
s = gTTS("Game over", lang="en")
s.save("audios_level/gameOver.mp3")  

s = gTTS("perú", lang="es-ES")
s.save("audios/peru.mp3") 
