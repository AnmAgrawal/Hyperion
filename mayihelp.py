import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import wolframalpha
import json
import requests
from tkinter import *
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

engine.setProperty('rate', 150)
engine.setProperty('volume', 1.5)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(audio, hindi):
    if hindi:
        hindi_audio = Translator().translate(audio).text
        audio = hindi_audio
    engine.say(audio)
    engine.runAndWait()

def exit():
    var.set('your personal assistant is shutting down,Good bye')
    speak('your personal assistant is shutting down,Good bye')
    window.update()
    window.destroy()

def wishme():
    '''
    This function wish the user according to time.
    '''
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        var.set("Good Morning !!")
        window.update()
        speak("Good Morning")

    elif hour>=12 and hour<18:
        var.set("Good Afternoon !!")
        window.update()
        speak("Good Afternoon")
    
    else:
        var.set("Good Evening !!")
        window.update()
        speak("Good Evening")
    var.set("I am your virtual Assistant. Please tell me how may i help you")
    speak("I am your virtual Assistant. Please tell me how may i help you")
    
def takeCommand():
    '''
    This function takes microphone input from user and returns string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        var.set("Recognizing...")
        window.update()
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        return "None"
    var1.set(query)
    window.update()
    return query
def  takeCommandInEnglish():
    """This function takes microphone input from user and converts it to string output"""
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()
        print("Listening")
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
    try:
        var.set("Recognizing...")
        window.update()
        print("Recognizing")
        english_query = recognize.recognize_google(audio, language='en-in')
        print(f"User said :{english_query}\n")
    except Exception as e:
        print(e)
        var.set("Please repeat")
        window.update()
        return "None" 
    var1.set(english_query)
    window.update()
    return english_query

def  takeCommandInHindi():
    """This function takes microphone input from user and converts it to string output"""
    print("hindi function")
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("...")
        window.update()
        print("Listening")
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
    try:
        var.set("...")
        window.update()
        print("Recognizing")
        
        translator = Translator()
        hindi_query = recognize.recognize_google(audio, language='hi-In')
        print(f"in hindi : {hindi_query}\n")
        query = translator.translate(hindi_query, dest='en')
        print(query.src)
        print(f"User said :{query.text}\n")
    except Exception as e:
        print(e)
        var.set("hindi")
        return "None" 
    var1.set(query.text)
    return query.text


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('chanchalbillore57@gmail.com', 'Supari%&')
    server.sendmail('chanchalbillore57@gmail.com', to, content)
    server.close()

def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    hindi = False
    translator = Translator()
    btn1.configure(bg = 'orange')
    wishme()
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
        btn1.configure(bg = 'orange')
        if 'Hindi' in language:
            hindi = True
            query = takeCommandInHindi().lower()
            if 'exit' in query:
                var.set("Bye sir")
                btn1.configure(bg = '#5C85FB')
                btn2['state'] = 'normal'
                btn0['state'] = 'normal'
                window.update()
                speak("Bye sir")
                break
        else:
            query = takeCommandInEnglish().lower()
            if 'exit' in query:
                var.set("Bye sir")
                btn1.configure(bg = '#5C85FB')
                btn2['state'] = 'normal'
                btn0['state'] = 'normal'
                window.update()
                speak("Bye sir")
                break

        #Logic for executing tasks based on query
        if 'wikipedia' in query:
            if 'open wikipedia' in query:
                webbrowser.open('wikipedia.com')
            else:
                try:
                    var.set("searching wikipedia...")
                    window.update()
                    speak("searching wikipedia",hindi)
                    speak("searching wikipedia")
                    query = query.replace("according to wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")
                    var.set(results)
                    window.update()
                    speak(results)
                except Exception as e:
                    var.set('sorry sir could not find any results')
                    window.update()
                    speak('sorry sir could not find any results')

        elif 'youtube' in query:
            webbrowser.open_new_tab("youtube.com")
        
        elif 'google' in query:
            webbrowser.open_new_tab("google.com")

        elif 'stack overflow' in query:
            webbrowser.open("stackoverflow.com", autoraise=True)

        elif 'play music' in query:
            music_dir = 'D:\\Songs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            var.set(f"Sir, the time is : {strTime}\n")
            window.update()
            speak(f"Sir, the time is {strTime}")
            print(f"Sir, the time is : {strTime}\n")

        elif 'open code' in query:
            codePath = "C:\\Users\\Anjali\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to anjali' in query:
            try:
                speak("what should i say?")
                content = takeCommand()
                to = "anjalichourishi999@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to sent email.")

        elif 'news' in query:
            news = webbrowser.open_new_tab("""wionews.com""")
            speak("Here are some headlines from the Times of India, Enjoy reading!!")

        elif 'search'  in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)

        elif 'ask' in query or "What" in query:
            var.set('I can answer to computational and geographical questions and what question do you want to ask now')
            window.update()
            speak('I can answer to computational and geographical questions  and what question do you want to ask now')
            question=takeCommand()
            app_id="KX6ALE-U6WK7L7K97"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            var.set(answer)
            window.update()
            speak(answer)
            print(answer)

        elif 'who are you' in query or 'what can you do' in query:
            var.set('I am MAYI HELP version 1 point O your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'In different cities, get top headline news from times of india and you can ask me computational or geographical questions too!')
            window.update()
            speak('I am MAYI HELP version 1 point O your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'In different cities, get top headline news from times of india and you can ask me computational or geographical questions too!')
            print('I am MAYI HELP version 1 point O your personal assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome, gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'In different cities, get top headline news from times of india and you can ask me computational or geographical questions too!')
       
        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by Anonymous")
            var.set("I was built by Anonymous")
            window.update()

        elif "weather" in query:
            api_key="b1667147637e9e31642fd01106b9eb63"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name?")
            var.set("What is the city name?")
            window.update()
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                var.set(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
                window.update()
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

        elif "goodbye" in query or "ok bye" in query or "stop" in query:
            speak('your personal assistant is shutting down,Good bye')
            var.set('your personal assistant is shutting down,Good bye')
            window.update()
            window.destroy()

def update(ind):
    frame = frames[(ind)%100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)

label2 = Label(window, textvariable = var1, bg = '#FAB60C')
label2.config(font=("Verdana", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable = var, bg = '#ADD8E6', height=5)
label1.config(font=("Courier", 20))
var.set('Welcome')
speak('Your Personal assistant is loading...... Please wait a minute')
print('Your Personal assistant is loading...... Please wait a minute')
label1.pack()

frames = [PhotoImage(file='robo.gif',format = 'gif -index %i' %(i)) for i in range(100)]
window.title('MAY-I-HELP')

label = Label(window, width = 400, height = 350)
label.pack()
window.after(0, update, 0)

btn0 = Button(text = 'WISH ME',width = 20, command = wishme, bg = '#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text = 'PLAY',width = 20,command = play, bg = '#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text = 'EXIT',width = 20, command = exit, bg = '#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()


window.mainloop()