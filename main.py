import pyttsx3
import speech_recognition as sr
import random
import requests, json

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()
r.energy_threshold = 1000

def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_current_weather(api_key, location):
    pass


def take_command():
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            command = r.recognize_sphinx(audio)
            return command.lower()
        except sr.UnknownValueError:
            talk("No input detected. Please try again.")
        except sr.RequestError:
            talk("I'm sorry, I'm currently unable to process your request. Please try again later.")
        except OSError as e:
            if "No Default Input Device Available" in str(e):
                talk("No audio input device found.")
                return input("Input command: ").lower()
            else:
                print("Other OSError:", e)


def startAI():
    greetings = ['Hey', 'Hello', 'Good day']
    talk(random.choice(greetings))

    while True:
        command = take_command()

        if 'hello' in command:
            talk("Hello to you too")
        elif 'help' in command:
            talk("I'm sorry, I didn't catch that. Can you please repeat?")
        elif 'weather' in command:
            api_key = "YOUR_API_KEY"
            location = "Port Harcourt"
            data = get_current_weather(api_key, location)
            if 'error' in data:
                talk("Sorry, I couldn't fetch the weather information.")
            else:
                temperature = data['current']['temp_c']
                condition = data['current']['condition']['text']
                talk(f"The current temperature in {location} is {temperature} degrees Celsius. It is {condition}.")
        else:
            talk("I'm sorry, I don't understand. Please try again.")

if __name__ == '__main__':
    startAI()
