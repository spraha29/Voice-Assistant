import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser 
import json
import requests
import pywhatkit
import re

engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    """ This function will programme voice assistant to speak something """
    engine.say(audio)
    engine.runAndWait()
    
def greeting():
    """This function will make your voice assistant greet you according to system time"""
    hour= int(datetime.datetime.now().hour)
    if hour>=6 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<17:
        speak("Good Afternoon")
    elif hour>=17 and hour<20:
        speak("Good Evening")
    else:
        speak("Good Night")
    speak("I am your voice assistant How may I help you")
    
def takeCommand():
    """This function takes microphone input from user and returns string output"""
    r= sr.Recognizer()
    with sr.Microphone() as source:
            print("Listening......")
            r.pause_threshold = 1
            audio = r.listen(source)
    try:
        print("Recognizing......")
        query= r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please....")
        return "None"
    return query

def wiki_search(query):
    """This function will provide information from wikipedia"""
    speak('Searching Wikipedia')
    query=query.replace("wikipedia","")
    results= wikipedia.summary(query,sentences=4)
    speak("According to Wikipedia")
    print(results)
    speak(results)
    
def open_website(query):
    """This function will open a website in web browser"""
    speak("Opening")
    webbrowser.open(f"{query}")

def news():
    """This function will read daily news"""
    speak("Select the kind of news you want to hear general business science entertainment sports")
    query= takeCommand().lower()
    speak("News for today is")
    if 'general' in query:
        url="https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=3e9fcb020feb44feaf631087d7265cd6"
    elif 'business' in query:
        url="https://newsapi.org/v2/top-headlines?sources=fortune&apiKey=3e9fcb020feb44feaf631087d7265cd6"
    elif 'science' in query:
        url="https://newsapi.org/v2/top-headlines?sources=new-scientist&apiKey=3e9fcb020feb44feaf631087d7265cd6"
    elif 'entertainment' in query:
        url="https://newsapi.org/v2/top-headlines?sources=buzzfeed&apiKey=3e9fcb020feb44feaf631087d7265cd6"
    elif 'sports' in query:
        url="https://newsapi.org/v2/top-headlines?sources=bbc-sport&apiKey=3e9fcb020feb44feaf631087d7265cd6" 
    news=requests.get(url).text
    news_dict= json.loads(news)
    arts= news_dict['articles']
    for article in arts:
        speak(article['title'])
    speak("Thanks for Listening")
    
def sending_msg(srch,msg):
    """This function will search phone number in text file and send message on whatsapp"""
    speak("Sending")
    with open("phone_numbers.txt") as f:
        details= f.read()
        search = re.compile(fr'\b{srch}.\d+')
        matches = search.finditer(details)
        for match in matches:
            l=list(match.span())
            phoneNumber= details[l[0]:l[1]].split(":")
        try:
            time_hour= int(datetime.datetime.now().hour)
            time_min= int(datetime.datetime.now().minute)+1
            pywhatkit.sendwhatmsg(f"+91{phoneNumber[1]}",f"{msg}",time_hour,time_min,25,True,5)
            speak("Message successfully sent")
        except Exception as e:
            speak("An Unexpected Error")
if __name__ == '__main__':
    greeting()
    while True:
        query= takeCommand().lower()
        if 'wikipedia' in query:
            wiki_search(query)
        elif 'open' in query:
            open_website(query)
        elif 'news' in query:
            news()
        elif 'message'in query:
            speak("Whom do you want to send message")
            srch= takeCommand().lower()
            speak("What message do you want to send")
            msg= takeCommand().lower()
            sending_msg(srch,msg)
        elif 'stop'in query:
            speak("Thank You and see you again")
            exit()
            