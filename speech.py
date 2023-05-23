import speech_recognition as sr
import openai
import pyttsx3
import pyaudio
import time
import os
import sys


openai.api_key = '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'

engine = pyttsx3.init()


def one(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except:
        print("skipping unknown error")


def two(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text


def three(text):
    engine.say(text)
    engine.runAndWait()


def four():
    while True:
        print("start")
        with sr.Microphone() as source:
            r = sr.Recognizer()
            audio = r.listen(source)
            try:
                t = r.recognize_google(audio)
                print(t)
                if t:
                        print(t)
                        print(f"you said {t}")
                        res = two(t)
                        print(f"gpt says {res}")
                        three(res)
                else:
                    three("I didn't Get it")

            except Exception as e:
                print("Error occured:{}".format(e))


def five():
    sys.exit("Stopped from talking")


if __name__ == "__main__":
    four()