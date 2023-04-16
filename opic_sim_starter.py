import sys
from opic_sim import Ui_MainWindow #수정부분
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import playsound
import time


class kinwriter(QMainWindow, Ui_MainWindow): 
    
    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.show()
        
        time.sleep(1)
        playsound.playsound('intro.wav')

app = QApplication([])
sn = kinwriter()
QApplication.processEvents()
sys.exit(app.exec_())

