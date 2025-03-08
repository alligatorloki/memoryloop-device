from gtts import gTTS
import pygame
import time
import datetime
import queue
import random
import re
#import pyflac
import sounddevice as sd
import os
from bleak import BleakClient
import speech_recognition as sr
pygame.init()
from bluepy.btle import Scanner
from pydub import AudioSegment, effects  
import pyaudio
from pydub import AudioSegment, effects  
from os import path

import wave
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
reminder = ""
filename = "output.wav"
adress = "dd:34:02: 0a:44:38"
scanner = Scanner()
devices = scanner.scan(3.0)
askedYet = False
p = pyaudio.PyAudio()  # Create an interface to PortAudio
r = sr.Recognizer()


frames = []  # Initialize array to store frames

startText = "Hello. I am going to ask you a question. Please answer to the best of your ability."
endText = "Thank you for answering these questions. That will be all"
startAudio = gTTS(startText)
endAudio = gTTS(endText)
startAudio.save('start.mp3')
endAudio.save('end.mp3')
print('ready')
def remindMeal():
    x = datetime.datetime.now()
    if(11>int(x.strftime("%H"))>6):
        reminder = ("By the way, have you had breakfast?")
    elif(16>int(x.strftime("%H"))>11):
        reminder = ("By the way, have you had lunch?")
    elif(20>int(x.strftime("%H"))>4):
        reminder = ("By the way, have you had dinner?")
    else:
        reminder = ""
    try:
        remidneraudio = gTTS(reminder)
        remidneraudio.save('result.mp3')
        reminderAud = pygame.mixer.Sound('result.mp3')
        songLength = reminderAud.get_length()
        pygame.mixer.music.load('result.mp3')
        print(reminder)
        pygame.mixer.music.play()
        time.sleep(songLength)
    except:
        print("failed whomp whomp")
class Fact:
    def __init__ (self,question,answer,box):
        self.question = question
        self.answer = answer
        
        self.box = box
    
    def askQuestion(self):
        frames = []
        print(self.question)
        response = ""
        questionAudio = gTTS(self.question)
        questionAudio.save('question.mp3')
        p = pyaudio.PyAudio()
        startpy = pygame.mixer.Sound("start.mp3")
        songLength = startpy.get_length()
        pygame.mixer.music.load('start.mp3')
        pygame.mixer.music.play()
        startpy.set_volume(1)
        time.sleep(songLength)
        qAudio = pygame.mixer.Sound('question.mp3')
        songLength = qAudio.get_length()
        pygame.mixer.music.load('question.mp3')
        
        pygame.mixer.music.play()
        qAudio.set_volume(1)
        time.sleep(songLength)
        stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk, exception_on_overflow = False)
            frames.append(data)
        

# Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        try:
            rawsound = AudioSegment.from_file("./output.wav", "wav")  
        except:
            print("idk man")
        normalizedsound = effects.normalize(rawsound)  
        normalizedsound.export("./balancedoutput.wav", format="wav")
        AUDIO_FILE = path.join(path.dirname(path.realpath('balancedoutput.wav')), "balancedoutput.wav")
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
        #response = r.recognize_sphinx(audio)
        #response = r.recognize_faster_whisper(audio)
        response = r.recognize_whisper(audio)
        #userAnswer = input("enter answer\n")
        userAnswer = response
        os.remove("./output.wav")
        os.remove("./balancedoutput.wav")
        
        if(re.search(self.answer,userAnswer,re.IGNORECASE)):
            result = ('correct, the answer is: ' + self.answer)
            self.box += 1
            resultAudio = gTTS(result)
            resultAudio.save('result.mp3')
            resAudio = pygame.mixer.Sound('result.mp3')
            songLength = resAudio.get_length()
            pygame.mixer.music.load('result.mp3')
            print(result)
            pygame.mixer.music.play()
            resAudio.set_volume(1)
            time.sleep(songLength)
            print(self.box)
        else:
            self.box = 1
            result = ('incorrect, the answer was: ' + self.answer + ', but you said: ' + userAnswer)
            resultAudio = gTTS(result)
            resultAudio.save('result.mp3')
            resAudio = pygame.mixer.Sound('result.mp3')
            songLength = resAudio.get_length()
            pygame.mixer.music.load('result.mp3')
            print(result)
            pygame.mixer.music.play()
            resAudio.set_volume(1)
            time.sleep(songLength)
            
            print(self.box)
        
   

day = 1
boxes = [7,6,5,4,3,2,1]
startQ = Fact(startText,"ok",0)
f1 = Fact("What is the third planet from the sun?","earth",1)
f2 = Fact("What is the longest river in the world?","nile",1)
f3 = Fact("Who wrote the cat in the hat?","dr. seuss",1)
f4 = Fact("what is the capital of France?","paris",0)
f5 = Fact("Fill in the blank: Roses are red, violets are :","blue",0)
f6 = Fact("Who gave the stature of liberty to the USA?","france",0)
f7 = Fact("what is The largest ocean animal?","blue whale",0)
futureFacts = []
askedQuestions = []
factArray = [f1,f3,f4,f5,f6,f7]


while day<=64:
        unaskedCount = 0
    
        print("day = ",day)
        i = 0
        
       
       
        askedYet = False
        prevRssi = 0
        while(askedYet == False):
            found = False
            devices = scanner.scan(1.0)
            for device in devices:
                if(device.addr == "dd:34:02:0a:44:38"):
                    print("DEV = {} RSSI = {}".format(device.addr, device.rssi))
                    found = True
                    if(device.rssi > -50 and prevRssi <= -50):
                        print("final if triggerd")
                        askedYet = True
                        
                    prevRssi = device.rssi
            if(found == False):
                prevRssi = -100000
        
       #THIS IS THE OLD CODE THAT KINDA WORKED
        
      
        #for x in factArray:
         #   unaskedCount = 0
          #  print(x.question)
           # if x not in askedQuestions:
            #    
             #   print("not in questions"+x.question)
              #  x.askQuestion()
               # askedQuestions.append(x)
                #break
            #else:
             #   unaskedCount += 1
        for x in factArray:
            
            print(x.question)
            if x not in askedQuestions:
                
                print("not in questions"+x.question)
                x.askQuestion()
                askedQuestions.append(x)
                break
            else:
                unaskedCount += 1
                if(unaskedCount == (factArray.__len__()-1)):
                    for y in factArray:
                        try:
                            askedQuestions.remove(y)
                        except:
                            print("failed")
       
        print(endText)
        endAudio1 = pygame.mixer.Sound('end.mp3')
        songLength = endAudio1.get_length()
        pygame.mixer.music.load('end.mp3')
        endAudio1.set_volume(1)
        pygame.mixer.music.play()
        time.sleep(songLength)
        
        remindMeal()

    


     
