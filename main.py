import objc
from Foundation import NSDate, NSRunLoop
import speech_recognition as sr
import webbrowser
from Cocoa import NSSpeechSynthesizer
import musiclibrary
import pyjokes
import requests
from openai import OpenAI



newsapi="0e2d3eabd3754aa0875f1c1d427ea287"

 

def tell_joke():
     joke = pyjokes.get_joke()
     print(joke)
     speak(joke)

def aiprocess(command):
    client = OpenAI(
    api_key="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"
)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis "},
    {"role": "user", "content": command}
  ]
)

    return (completion.choices[0].message.content)

recogniser=sr.Recognizer()
def speak(text):
    synth = NSSpeechSynthesizer.alloc().initWithVoice_(None)
    synth.startSpeakingString_(text)
    # Run a run loop until speech finishes
    while synth.isSpeaking():
        NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
def processCommand(c):
    if "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com") 
    elif c.lower().startswith("play"):
        print(c)
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)
    # elif c.lower().startswith("tell"):
    #       print(c)
    #       tell_joke()
    elif "how are you" in c.lower():
        speak("i am good , how are you")
    elif "Who are you" in c.lower():
        speak("i am Jarvis , your personal assistant")
   
        

    elif c.lower().startswith("news"):
        r=requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=0e2d3eabd3754aa0875f1c1d427ea287")
        if r.status_code == 200:
            data=r.json()

            articles=data.get('articles',[])

            for article in articles:
                speak(article['title'])

    else:  
        output = aiprocess(c) 
        speak(output)




if __name__ == "__main__":
    
    
    #Listen for the wake word Jarvis
    while True:
        r = sr.Recognizer()
        
# recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                 print("Listening!")
                 audio = r.listen(source , timeout=20 , phrase_time_limit=10 )
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("hello samay")
                #listen for Command
                with sr.Microphone() as source:

                    print("Jarvis active")
                    audio = r.listen(source, timeout=20 , phrase_time_limit=10 )
                    command=r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
             print("Sphinx could not understand audio")
        except sr.RequestError as e:
              print("Sphinx error; {0}".format(e))
        




