from elevenlabs import voices, generate
from elevenlabs import generate, play, set_api_key
import rich

audio = generate(
    text="Witaj świecie, jak się masz?",
    api_key="69629e2241ca3f96a3e97587ad5072e5",
    voice="Bella",
    model='eleven_multilingual_v2'
)
# play(audio)
play(audio, notebook=True)  # notebook=True - odtwarzanie w google colab

f = open("output.mp3", "wb")
f.write(audio)
f.close()