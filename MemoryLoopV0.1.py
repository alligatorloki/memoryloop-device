from gtts import gTTS
import pygame
import time
import os
from bleak import BleakClient
import speech_recognition as sr
pygame.init()
from bluepy.btle import Scanner
adress = "dd:34:02:0a:44:38"
scanner = Scanner()
devices = scanner.scan(3.0)
askedYet = False

r = sr.Recognizer()

startText = "Hello. I am going to ask you some questions. Please answer to the best of your ability. Say ok to continue"
endText = "Thank you for answering these questions. That will be all"
startAudio = gTTS(startText)
endAudio = gTTS(endText)
startAudio.save('start.mp3')
endAudio.save('end.mp3')
print('ready')
class Fact:
    def __init__ (self,question,answer,box):
        self.question = question
        self.answer = answer
        self.box = box
    
    def askQuestion(self):
        print(self.question)
        response = ""
        questionAudio = gTTS(self.question)
        questionAudio.save('question.mp3')
        qAudio = pygame.mixer.Sound('question.mp3')
        songLength = qAudio.get_length()
        pygame.mixer.music.load('question.mp3')
        pygame.mixer.music.play()
        time.sleep(songLength)
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            #response = r.recognize_sphinx(audio)
            response = r.recognize_vosk(audio)
        except sr.UnknownValueError:
            response = "Sphinx could not understand audio"
        except sr.RequestError as e:
            response = ("Sphinx error; {0}".format(e))
        #userAnswer = input("enter answer\n")
        userAnswer = response
        if(userAnswer == self.answer):
            result = ('correct, the answer is: ' + self.answer)
            self.box += 1
            resultAudio = gTTS(result)
            resultAudio.save('result.mp3')
            resAudio = pygame.mixer.Sound('result.mp3')
            songLength = resAudio.get_length()
            pygame.mixer.music.load('result.mp3')
            print(result)
            pygame.mixer.music.play()
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
            time.sleep(songLength)
            
            print(self.box)
   

day = 1
boxes = [7,6,5,4,3,2,1]
f1 = Fact("What is the third planet from the sun?","earth",1)
f2 = Fact("What is the longest river in the world?","the nile",1)
f3 = Fact("Who wrote the cat in the hat?","Dr Seuss",1)
f4 = Fact("what is the capital of France?","paris",0)
f5 = Fact("Fill in the blank: Roses are red, violets are :","blue",0)
futureFacts = [f4,f5]
factArray = [f1,f2,f3]

while day<=64:
    userInput = input()
    if(userInput == "day"):
        print("day = ",day)
        i = 0
        if(day != 0):
            while i<2 and len(futureFacts) > 0:
                futureFacts[0].box = 1
                factArray.append(futureFacts[0])
                futureFacts.pop(0)
        askedYet = False
        prevRssi = 0
        while(askedYet == False):
            devices = scanner.scan(3.0)
            for device in devices:
                if(device.addr == "dd:34:02:0a:44:38"):
                    print("DEV = {} RSSI = {}".format(device.addr, device.rssi))
                    if(device.rssi > -50 and prevRssi <= -50):
                        print("final if triggerd")
                        askedYet = True
                    prevRssi = device.rssi
                    
        print(startText)
        startAudio = pygame.mixer.Sound('start.mp3')
        songLength = startAudio.get_length()
        pygame.mixer.music.load('start.mp3')
        
        pygame.mixer.music.play()
        time.sleep(songLength)
        
        aknowledged = False
        while aknowledged == False:
            input2 = input()
            if(input2 == 'ok'):
                aknowledged = True
        for x in boxes:
            checkVal = float(day/pow(2,(x-1)))
            #print(checkVal)
            if checkVal.is_integer() == True:
               print("\n*******BOX ",x,"*******")
               for y in factArray:
                   if(y.box == x):
                        y.askQuestion()
       # for x in factArray:
            #print(x.box)
        #    checkVal = float(day/pow(2,(x.box-1)))
         #   print(checkVal)
          #  if checkVal.is_integer() == True:
           #     print("\n*******BOX ",x.box,"*******")
            #    print("true")
             #   x.askQuestion()
        print(endText)
        endAudio1 = pygame.mixer.Sound('end.mp3')
        songLength = endAudio1.get_length()
        pygame.mixer.music.load('end.mp3')
        
        pygame.mixer.music.play()
        time.sleep(songLength)
        day += 1

    if(userInput == "end"):
        day = 65
    if(userInput == 'set'):
        print('what day?')
        dayInput = input()
        day = input    


     
