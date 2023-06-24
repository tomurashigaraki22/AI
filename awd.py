import pyttsx3
import speech_recognition as sr
import random
import requests, json
import pygame, difflib, os
import wikipedia
import time
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 2)
rate = engine.getProperty('rate')


r = sr.Recognizer()
r.energy_threshold = 1000
available_songs = os.listdir('C:/Users/Emmanuel Gbodo-Otiki/Music/')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def searchWiki(query):
    name = wikipedia.summary(query)
    print(name)
    talk(name)
    time.sleep(0.5)

def find_closest_song(requested_song, available_songs):
    closest_song = difflib.get_close_matches(requested_song, available_songs, n=3, cutoff=0.3)
    if closest_song:
        return closest_song[0]
    else:
        return None


def get_current_weather(api_key, location):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + location + "&appid=" + api_key
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        error_code = response.status_code
        with open("error_log.txt", "a") as file:
            file.write(f"Error: {error_code}\n")
        return None
    
def play_song(path):
    closest_songs = find_closest_song(path, available_songs)
    print(closest_songs)
    if closest_songs:
        closest_song = closest_songs
        path = f"C:/Users/Emmanuel Gbodo-Otiki/Music/{closest_song}"
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            talk(f"Playing {closest_song}")
        except pygame.error as e:
            print("Error: ", str(e))
            talk("Sorry, there was an error playing the song.")
    else:
        talk("No matching songs found.")

def pause_song():
    try:
        pygame.mixer.music.pause()
    except pygame.error as e:
        print("Error in playing...")

def resume_song():
    try:
        pygame.mixer.music.unpause()
    except pygame.error as e:
        print("Error in playing...")

def stop_song():
    try:
        pygame.mixer.music.stop()
    except pygame.error as e:
        print("Error in playing...")


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
                print("No audio input device found.")
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
            api_key = "60ee721858cf9f5181c351c197fb045e"
            location = "Port Harcourt"
            data = get_current_weather(api_key, location)
            if data is None:
                talk("Sorry, I couldn't fetch the weather information.")
                startAI()
            else:
                temperature = data['main']['temp']
                report = data['weather'][0]['description']
                engine.setProperty('rate', rate - 20)
                talk(f"The temperature in {location} is {temperature} degree kelvin and the weather is {report}")
        elif 'play' in command:
            song_name = command.split('play', 1)[1].strip()
            paths = f"C:/Users/Emmanuel Gbodo-Otiki/Music/{song_name}.mp3"
            play_song(paths)
        elif 'pause' in command:
            pause_song()
        elif 'resume' in command:
            resume_song()
        elif 'stop' in command or 'quit' in command:
            stop_song()
        elif 'search' in command:
            if "for" in command:
                command = command.replace("search for", "")
                searchWiki(command)
            else:
                command = command.replace("search", "")
                searchWiki(command)
        elif 'exit' in command:
            quit
        elif 'open youtube' in command:
            webbrowser.open_new_tab("www.youtube.com")
            talk("Youtube is now open")
            time.sleep(0.5)
        elif 'open gmail' in command:
            webbrowser.open_new_tab("www.gmail.com")
            talk("Gmail is now open")
            time.sleep(0.5)
        elif 'open google' in command:
            webbrowser.open_new_tab("www.google.com")
            talk("Google is now open")
            time.sleep(0.5)
        elif 'open' in command:
            command = command.replace("open ", "")
            webbrowser.open_new_tab(command)
            talk(command + "is now opened")
            time.sleep(0.5)
        else:
            talk("I'm sorry, I don't understand. Please try again.")

if __name__ == '__main__':
    startAI()
