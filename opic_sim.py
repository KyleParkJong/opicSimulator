import numpy as np
import pyaudio
from scipy.io import wavfile
from scipy import signal
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
import playsound
import random
import datetime

import resources
from PyQt5 import QtCore, QtGui, QtWidgets



# 질문 리스트
opicQuestions = [
    # Intro
    'Tell me about yourself.',
    
    # Dental clinic
    'Describe a dental clinic in detail.',
    'When was the last time you went to a dentist? How was the doctor? What was the atmosphere of the place like?',
    'Kids are usually afraid of going to a dentist. How about you? Is there an event you remember? Tell me about it.',
    
    # ID cards
    'What kind of identification cards do you have now? When do you use those cards?',
    'Have you ever been in a situation that you were in trouble because you didn\'t have your ID card? When was it? What happended? Tell me in detail.',
    'I\'d like to know about the steps you have to take to get an identification card ID. Give me a detailed description of the steps you need to take in order to get it',
    'Let\'s talk about the first identification card. You got what kind of ID card was it? How did you feel when you got the ID card? Tell me in detail.',
    
    # Weather
    'How different are the seasonal weather is? How is it different depending on the four seasons?',
    'What kinds of outdoor activities do people in your country attend depending on the weather?',
    'Tell me about the memorable experience that happened in a season. What happened? Why is it so memorable? How did the weather affect the event?',

    # Neighbor
    'Tell me about your neighborhood. What is it like to live in that part of town?',
    'Describe your neighbors. Who is your closest neighbor? How aften do you meet your neighbor? And what do you do with him or her?',
    'Tell me about your neighbors and there routines. Tell me about the kids, adults and the older people.',
    
    # House(furniture)
    'Think about the day you moved into your house. How different was it from now? What has changed? Tell me about it.',
    'What are the things you did to change your home? Did you buy new furniture or paintings? Tell me about everything you did.',
    'Tell me about an obvious weakness about your house. Also, if you want to move to another place, what kind of house do you want to move into?',
    'Tell me about problems you experienced in your home. Did something break or did you have to call a repairman? Describe the problem in detail.',
    'Tell me about the furniture in your house. I\'d like to know detailed information of the furniture in your house.',   
    'What home appliances do people use? Refrigerators and dishwashers? What else can you think of?',
    'How do you usually decide what to wear? Do you wear different clothes during the week and the weekend?',

    # Work
    'Tell me how the people in your city commute to work. Are there any different ways for people to travel?',
    'Have you ever experienced any interesting or frustrating thing when going to work? Maybe you experience the car breaking down. Tell me about the memorable experience in as many details as possible.',
    
    # Movie
    'You indicated that you like to see movies. Who is your favorite actor or actress? And why?',
    'Describe the theater you go to. What does it look like? Why do you like going there? Tell me everything you can remember.',
    'What kind of activites do you do before, during and after the movie? Tell me about your typical day when watching a movie.',
    'When was the last time you went to the movie theater? What kind of movie did you see? Where did you go? And who were you with? Was it interesting? Tell me about it in as many details as possible.',
    
    # Concert
    'How often do you go to concerts? Who do you usually go with? What do you do before and after the concerts?',
    'What kind of concert do you like to attend? Why? And do you prefer concerts with seating or no seating? Why?',
    'How did you become interested in concerts?',
    'Tell me about the last concert you went to? When was it? Resume, how was it?',
    
    # Park
    'You indicated that you go to a park. Where is it located? Describe the park you like to go to in detail.',
    'What kind of activities do you usually do at the park? Tell me about everything you do at a park from the time you arrive at a park to the time you leave the park.',
    'Describe the last time you went to a park. When was it with whom was last weekend?',
    'Tell me about a memorable event that happened at the park you often go to. When was it? What was the event about? What did you do there at that time? Why was it so memorable? Tell me in as much detail as you can.',
    
    # Game
    'What kind of game do you usually play when where and with whom?',
    'Tell me about your favorite game. Why do you like it? Tell me the rules of the game.',
    'I also like to play games. Ask me three to four questions about games.',
    'Describe the game, you recently played. What was it? What happened?',
    'Which do you prefer the game you play by yourself or together with other people? Why?',
    'What is the popular game in Korea? Why is it so popular?',
    
    # Cook
    'What kind of food do you like to cook? Why? Tell me how to cook.',
    'How often do you cook? When and where do you usually cook?',
    'Tell me about the first time you cooked. What was it? How did it taste?',
    'Maybe something unexpected happened, when you cooked. Tell me about your experience with details. What kind of food did you cook? And what was wrong with it?',
    
    # Music
    'How often do you listen to music? When and where do you usually listen to music? What kind of music device do you use when listening to music? Tell me all the details.',
    'What kind of music do you like? Why, who is your favorite singer or composer?',
    'When and how did you first become interested in listening to music? Was there a special reason? If so, why?',
    'Tell me about the special moments or episodes, you\'ve experienced while listening to music.'

]

qNum = 5             # 문제 개수 설정
recordTime = 60      # 한 문제 당 녹음 시간 설정, 120 seconds
randQuestions = random.sample(opicQuestions, qNum)     # 지정한 수 만큼 랜덤으로 문제 고른다.
i = 0
j = 1

RATE = 16000    
CHUNK = RATE*recordTime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        # Main
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # avaLabel
        self.avaLabel = QtWidgets.QLabel(self.centralwidget)
        self.avaLabel.setGeometry(QtCore.QRect(174, 59, 40, 20))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.avaLabel.setFont(font)
        self.avaLabel.setObjectName("avaLabel")
        
        # avaImg
        self.avaImg = QtWidgets.QLabel(self.centralwidget)
        self.avaImg.setGeometry(QtCore.QRect(30, 100, 330, 330))
        self.avaImg.setStyleSheet("image: url(:/img/img/Ava.jpg);")
        self.avaImg.setText("")
        self.avaImg.setPixmap(QtGui.QPixmap(":/avaImg/과제/img/Ava.png"))
        self.avaImg.setScaledContents(True)
        self.avaImg.setObjectName("avaImg")
        
        # nextButton
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(749, 530, 121, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        
        # exitButton
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(640, 530, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.exitButton.setFont(font)
        self.exitButton.setObjectName("exitButton")
        
        # replayButton
        self.replayButton = QtWidgets.QPushButton(self.centralwidget)
        self.replayButton.setGeometry(QtCore.QRect(150, 450, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.replayButton.setFont(font)
        self.replayButton.setObjectName("replayButton")
        
        # recordingDisplay
        self.recordingDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.recordingDisplay.setGeometry(QtCore.QRect(500, 240, 271, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(50)
        self.recordingDisplay.setFont(font)
        self.recordingDisplay.setObjectName("recordingDisplay")
        self.recordingDisplay.setText("Answer the questions for " + str(recordTime) + " seconds as soon as Ava finishes talking.")
        
        # numDisplay
        self.numDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.numDisplay.setGeometry(QtCore.QRect(770, 20, 101, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(50)
        self.numDisplay.setFont(font)
        self.numDisplay.setObjectName("numDisplay")
        self.numDisplay.setText('  1 / '+ str(qNum))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.exitButton.clicked.connect(MainWindow.exit)
        self.nextButton.clicked.connect(MainWindow.next)
        self.replayButton.clicked.connect(MainWindow.replay)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # 시작/다음 질문 버튼
    def next(self):
        global i, j
        self.displayChange()    # 문제 번호 표시
        
        question = randQuestions[i]
        fileName = 'Q' + str(j) + '.wav'
        
        # TTS
        tts = gTTS(text=question, lang='en')
        tts.save(fileName)
        
        d, fs = sf.read(fileName)
        ds = signal.resample(d, int(len(d)*16/24))
        sf.write('./questions/'+fileName, ds, 16000)        # questions 폴더에 질문 저장
        playsound.playsound('./questions/'+fileName)
        
        # ASR
        fileName2 = 'A' + str(j) + '.wav'
        p=pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=RATE, 
                input=True, 
                frames_per_buffer=CHUNK,
                input_device_index=0)
        
        
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        wavfile.write('./record/'+fileName2, RATE, data.astype(np.int16))       # record 폴더에 녹음한 답안 저장
        
        r = sr.Recognizer()
        wavr = sr.AudioFile('./record/'+fileName2)
        
        fileName3 = 'A' + str(j) + '.txt'
        f = open('./script/'+fileName3, 'w')        # script 폴더에 녹음된 답안이 txt 파일 형태로 저장
        
        with wavr as source:
            audio = r.record(source)
            f.write(r.recognize_google(audio))
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        f.close()
        
        i = i + 1
        j = j + 1
        
    # 종료 버튼
    def exit(self):    
        MainWindow.close()

    # 질문 다시 듣기 버튼
    def replay(self):      
        fileName = 'Q' + str(j-1) + '.wav'
        playsound.playsound(fileName)
    
    def displayChange(self):
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(50)
        self.numDisplay.setFont(font)
        self.numDisplay.setText(str(j) + ' / ' + str(qNum))
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Opic simulator", "Opic simulator"))
        self.avaLabel.setText(_translate("MainWindow", "Ava"))
        self.nextButton.setText(_translate("MainWindow", "Start / Next"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.replayButton.setText(_translate("MainWindow", "Replay"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

