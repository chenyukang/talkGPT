import speech_recognition as sr
import os
import openai
import subprocess
import argparse


LANGUAGES = {
    "en": "english",
    "zh-hans": "chinese"
}

def talk(language):
    print("Listening...")
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print(audio)
        transcript = r.recognize_whisper(audio, language=language)
        print(transcript)
        return transcript

def send_request(language, words):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": words}
      ]
    )
    answer = completion.choices[0].message["content"]
    print(answer)
    voice = ""
    if language == "chinese":
        voice = "--voice Tingting"
    cmd_str = "say " + voice +  " \"" + answer.replace("\n", " ") + "\""
    subprocess.call(cmd_str, shell=True)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
        "--language",
        type=str,
        choices=sorted(LANGUAGES.keys()),
        default="en",
        metavar="LANGUAGE",
        help="language to talk, available: {%(choices)s}",
  )
  options = parser.parse_args()
  language = LANGUAGES[options.language]
  print(language)
  while True:
      input_words = talk(language)
      send_request(language, input_words)
