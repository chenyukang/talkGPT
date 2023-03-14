import argparse
import os
import openai
import subprocess
import speech_recognition as sr


LANGUAGES = {
  "en": "english",
  "zh-hans": "chinese"
}

def talk(language):
  
    print("\n\nListening...")
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print(audio)
        
        transcript = recognizer.recognize_whisper(audio, language=language)
        print(transcript)
        
        return transcript


def send_request(language, words):
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0301",
      messages=[
        {
            "role": "user", 
            "content": words
        }
      ]
    )
    
    answer = completion.choices[0].message["content"]
    print(answer)
    
    voice = ""
    if language == "chinese":
        voice = "--voice Tingting"
    
    out = answer.replace('\n', " ")
        
    cmd_str = f"say {voice} \"{out}\""
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
