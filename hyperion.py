import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from sys import platform
from googletrans import Translator

if platform == "linux" or platform == "linux32":
    """This initializes the pyttsx3 engine with espeak for linux"""
    engine = pyttsx3.init('espeak')
elif platform == "darwin":
    """This initializes the pyttsx3 engine with NSSpeechSynthesizer on Mac OS X"""
    engine = pyttsx3.init('nsss')
else:
    """This initializes the pyttsx3 engine with microsoft sapi5"""
    engine = pyttsx3.init('sapi5') #sapi5 is used to use the default voices present in windows

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.5)

def speak(audio):
    """This function converts the text in audio to speech and says it"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """This function wishes the user based on the current system time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good morning')
    elif hour >=12 and hour < 18:
        speak('Good afternoon')
    else:
        speak('Good evening')

    speak('I am Hyperion sir. How may I help you')

def  takeCommandInEnglish():
    """This function takes microphone input from user and converts it to string output"""
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
    try:
        print("Recognizing")
        english_query = recognize.recognize_google(audio, language='en-in')
        print(f"User said :{english_query}\n")
    except Exception as e:
        print(e)
        print("Please repeat")
        return "None" 
    return english_query

def  takeCommandInHindi():
    """This function takes microphone input from user and converts it to string output"""
    print("hindi function")
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
    try:
        print("Recognizing")
        
        translator = Translator()
        hindi_query = recognize.recognize_google(audio, language='hi-In')
        print(f"in hindi : {hindi_query}\n")
        query = translator.translate(hindi_query, dest='en')
        print(query.src)
        print(f"User said :{query.text}\n")
    except Exception as e:
        print(e)
        print("Please repeat")
        return "None" 
    return query.text

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vyom.mitra1@gmail.com', 'do_what_you_can\'t1')
    server.sendmail('vyom.mitra1@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    speak("Choose your language - hindi or english")
    recognize = sr.Recognizer()
    language = ""
    query = ""
    with sr.Microphone() as source:
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
        language = recognize.recognize_google(audio, language='en-IN')
    print("selected - ",language)
    while True:
        if 'Hindi' in language:
            query = takeCommandInHindi().lower()
        else:
            query = takeCommandInEnglish().lower()
        
    #Logic for executing tasks
        if 'wikipedia' in query:
            speak('Searching wikipedia')
            query.replace('wikipedia','')
            results = wikipedia.summary(query, sentences=3)
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com",new=0, autoraise=True)
        elif 'open google' in query:
            webbrowser.open("www.google.com",new=0, autoraise=True)
        elif 'play music' in query:
            music_dir = 'D:\\Songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is{strtime}")
        elif 'open code' in query:
            path = "D:\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
        elif 'send email' in query:
            try:
                speak('give your massage')
                content = takeCommandInEnglish()
                to = "anmolagrawal19@outlook.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e.__cause__)
                speak("Email couldn't be sent")

        elif 'quit' in query or 'bye' in query:
            exit()
