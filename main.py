import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai 
from gtts import gTTS
import pygame
import os

 
# print(sr.Microphone.list_microphone_names())
# recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="05374abd905f47e4bfb6517c41f510e3"

genai.configure(api_key="your key")


def speak_old(text):
    engine.say(text)
    engine.runAndWait()



def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

     # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def aiProcess(command):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Use an available model
    
    response = model.generate_content(command)   # Proper format
    return response.text[:100]  # Extract the response correctly


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
    # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 


if __name__=="__main__":
    speak("Initiallizing Jarvis...")
    while True:
    #For wake word Jarvix
    # obtain audio from the microphone
        r = sr.Recognizer()
     
        

# recognize speech using Jarvis
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("listening!")
                audio = r.listen(source , timeout=2, phrase_time_limit=1  )
            command=r.recognize_google(audio)
            if(command.lower()=="hello"):
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis Active !")
                    audio = r.listen(source )
                    command=r.recognize_google(audio)

                    processCommand(command)

                    
        except sr.UnknownValueError:
            print("Could not understand audio, please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        
        
