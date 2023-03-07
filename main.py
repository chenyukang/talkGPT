import speech_recognition as sr
import os
import openai
import subprocess

def talk():
    print("Listening...")
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print(audio)
        transcript = r.recognize_whisper(audio, language="english")
        print(transcript)
        return transcript

def send_request(words):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": words}
      ]
    )
    print(completion.choices[0].message)
    cmd_str = "say \"" + completion.choices[0].message["content"].replace("\n", " ") + "\""
    subprocess.call(cmd_str, shell=True)

while True:
    input_words = talk()
    send_request(input_words)
