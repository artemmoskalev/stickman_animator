'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QLabel, QLineEdit, QWidget, QTimer, QIcon, QFrame, QDoubleSpinBox, QSize
from PyQt5.QtCore import Qt

from stickman.UI.AssetManager import assets

"""
    ---------------------------------------

    ClASS RESPONSIBLE SHOWING INPUT LINE WITH LABEL AND OK-Cancel BUTTONS
    
    ---------------------------------------

"""         
class InputLine(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        
        component_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                                .QLabel {
                                    padding-top: 7px;
                                    font-weight: bold;
                                    font-size: 14px;
                                }
                                .QLineEdit {
                                    font-weight: bold;
                                    font-size: 14px;
                                }
                                .QLabel#error {
                                    color: red;
                                    font-size: 12px;
                                    font-style: italic;
                                    padding-top: 0px;
                                    padding-left: 6px;
                                }   
                            """       
               
        self.label = QLabel("", self)
        self.label.setStyleSheet(component_stylesheet)
        self.label.setAlignment(Qt.AlignRight)
        self.label.resize(170, 30)
        self.label.move(0, 0)        
        
        self.text = QLineEdit(self)
        self.text.setStyleSheet(component_stylesheet)
        self.text.resize(200, 30)
        self.text.move(175, 0)
        
        self.ok = QPushButton("OK", self)
        self.ok.setStyleSheet(component_stylesheet)
        self.ok.resize(100, 30)
        self.ok.move(380, 0)
        
        self.cancel = QPushButton("Cancel", self)
        self.cancel.setStyleSheet(component_stylesheet)
        self.cancel.resize(100, 30)
        self.cancel.move(485, 0)
    
        self.error = QLabel("", self)
        self.error.setObjectName("error")
        self.error.setStyleSheet(component_stylesheet)
        self.error.resize(250, 30)
        self.error.move(595, 0)
    
    """ listeners which control what happens on ok an cancel button presses """
    def addOkListener(self, onOkEvent):
        self.ok.clicked.connect(onOkEvent)
    def addCancelListener(self, onCancelEvent):
        self.cancel.clicked.connect(onCancelEvent)
        
    """ utility methods of the widget """
    def getText(self):
        return self.text.text()
    def setText(self, text):
        self.text.setText(text)        
        
    def setLabelText(self, text):
        self.label.setText(text)
        
    def setErrorText(self, text):
        self.error.setText(text)

"""
    ---------------------------
    CLASS FOR STORING MAPPINGS BETWEEN BUTTONS AND FRAMES. SIMPLIFIED VERSION OF DICT
    ---------------------------
"""
class FrameMap():
    
    def __init__(self):
        self.buttons = list()
        self.active = None
        self.frames = list()
    
    def __delitem__(self, key):
        index = self.buttons.index(key)
        self.buttons.remove(key)
        del self.frames[index]
        if self.active == key:
            self.active = None
        
    def __getitem__(self, key):
        return self.frames[self.buttons.index(key)]
        
    def __setitem__(self, key, value):
        self.buttons.append(key)
        self.frames.append(value)
    
    def __len__(self):
        return len(self.buttons)
    
    def keys(self):
        return self.buttons
    
    def index(self, key):
        return self.buttons.index(key)
    
    def insertAt(self, index, key, value):
        self.buttons.insert(index, key)
        self.frames.insert(index, value)
    
    def setActive(self, key):
        self.active = key
        
    def isActive(self, key):
        if self.active == key:
            return True
        else:
            return False     
        
"""
    ---------------------------
    CLASS RESPONSIBLE FOR STORING FRAME DATA
    ---------------------------
"""
class Frame():
    
    def __init__(self, time):
        self.time = time
        self.stickmen = list()
        
"""
    -------------------------------
        CLASS WHICH REPRESENTS THE INPUT LINE FOR TIME CHANGING FOR FRAMES
    -------------------------------
"""
class TimeInputLine(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()       
    
    def initUI(self):
        self.resize(400, 47)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        component_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                                .QDoubleSpinBox {
                                    font-weight: bold;
                                    font-size: 23px;
                                }
                                .QLabel {
                                    font-weight: bold;
                                    font-size: 23px;
                                }
                            """
        
        self.label = QLabel("", self)
        self.label.resize(174, 43)
        self.label.move(2, 2)
        self.label.setStyleSheet(component_stylesheet)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.show()       
        
        self.spinbox = QDoubleSpinBox(self)
        self.spinbox.setRange(0.1, 10)
        self.spinbox.setValue(0.5)
        self.spinbox.setSingleStep(0.5)
        self.spinbox.setDecimals(1)
        self.spinbox.resize(100, 43)
        self.spinbox.move(176, 2)
        self.spinbox.setStyleSheet(component_stylesheet)
        self.spinbox.show()
        
        self.enter = QPushButton("", self)
        self.enter.setIcon(assets.enter)
        self.enter.setIconSize(QSize(35, 35))
        self.enter.resize(60, 43)
        self.enter.move(278, 2)  
        self.enter.setStyleSheet(component_stylesheet)
        self.enter.show()
        
        self.cancel = QPushButton("", self)
        self.cancel.setIcon(assets.exit)
        self.cancel.setIconSize(QSize(35, 35))
        self.cancel.resize(60, 43)
        self.cancel.move(338, 2)     
        self.cancel.setStyleSheet(component_stylesheet) 
        self.cancel.show()
    
    """ listeners which control what happens on accept and on cancel button presses """
    def addAcceptListener(self, onAcceptListener):
        self.enter.clicked.connect(onAcceptListener)
    def addCancelListener(self, onCancelListener):
        self.cancel.clicked.connect(onCancelListener)   
    

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SHOWING DIGITAL CLOCK
    
    ---------------------------------------

"""       
class Clock(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        clock_stylesheet = """
                                .QLabel {
                                    padding-top: 10px;
                                    font-weight: bold;
                                    font-size: 25px;
                                    color:#ff5e5e;
                                }
                            """  
        
        self.accumulator = 0
        
        self.time = QLabel("0:00.0", self)
        self.time.resize(140, 45)
        self.time.setStyleSheet(clock_stylesheet)
        self.time.setAlignment(Qt.AlignHCenter)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)        
    
    def startClock(self):
        self.timer.start(100)
        
    def stopClock(self):
        self.timer.stop()
    
    def reset(self):
        self.accumulator = 0
        self.time.setText("0:00.0")
    
    def updateTime(self):
        self.accumulator = self.accumulator + 1
        self.time.setText(str(int(self.accumulator%6000/600)) +":"+str(int(self.accumulator%600/100))+str(int(self.accumulator%100/10))+"."+str(self.accumulator%10))
               
