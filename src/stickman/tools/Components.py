'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QLabel, QLineEdit, QWidget, QTimer, QFrame, QDoubleSpinBox, QSize
from PyQt5.QtCore import Qt

from stickman.UI.AssetManager import assets
import copy

"""
    ---------------------------------------

    ClASS RESPONSIBLE SHOWING INPUT LINE WITH LABEL AND OK-Cancel BUTTONS
    
    ---------------------------------------

"""         
class InputLine(QWidget):
    
    HEIGHT = 30
    LABEL_WIDTH = 170
    INPUT_TEXT_WIDTH = 200
    BUTTON_WIDTH = 100
    BUTTON_BLOCK_X = 380
    ELEMENT_GAP = 5
    
    ERROR_WIDTH = 250
    ERROR_X = 595
    
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
        self.label.resize(InputLine.LABEL_WIDTH, InputLine.HEIGHT)
        self.label.move(0, 0)        
        
        self.text = QLineEdit(self)
        self.text.setStyleSheet(component_stylesheet)
        self.text.resize(InputLine.INPUT_TEXT_WIDTH, InputLine.HEIGHT)
        self.text.move(InputLine.LABEL_WIDTH + InputLine.ELEMENT_GAP, 0)
        
        self.ok = QPushButton("OK", self)
        self.ok.setStyleSheet(component_stylesheet)
        self.ok.resize(InputLine.BUTTON_WIDTH, InputLine.HEIGHT)
        self.ok.move(InputLine.BUTTON_BLOCK_X, 0)
        
        self.cancel = QPushButton("Cancel", self)
        self.cancel.setStyleSheet(component_stylesheet)
        self.cancel.resize(InputLine.BUTTON_WIDTH, InputLine.HEIGHT)
        self.cancel.move(InputLine.BUTTON_BLOCK_X + InputLine.BUTTON_WIDTH + InputLine.ELEMENT_GAP, 0)
    
        self.error = QLabel("", self)
        self.error.setObjectName("error")
        self.error.setStyleSheet(component_stylesheet)
        self.error.resize(InputLine.ERROR_WIDTH, InputLine.HEIGHT)
        self.error.move(InputLine.ERROR_X, 0)
    
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
    
    def first(self):
        if len(self.buttons) > 0:
            return self.buttons[0]
        else: 
            return None
        
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
    
    def nextValue(self, value):
        index = self.frames.index(value)
        if not index + 1 > len(self.frames)-1:
            return self.frames[index+1]
        else:
            return None
    
"""
    ---------------------------
    CLASS RESPONSIBLE FOR STORING FRAME DATA
    ---------------------------
"""
class Frame():
    
    def __init__(self, time):
        self.time = time
        self.stickmen = list()
        
    def copy(self):
        copy_frame = Frame(self.time)
        copy_frame.stickmen = copy.deepcopy(self.stickmen)
        return copy_frame
    
    def getStickman(self, name):
        for stickman in self.stickmen:
            if stickman.name == name:
                return stickman
        return None
        
"""
    -------------------------------
        CLASS WHICH REPRESENTS THE INPUT LINE FOR TIME CHANGING FOR FRAMES
    -------------------------------
"""
class TimeInputLine(QFrame):
    
    WIDTH = 396
    HEIGHT = 43
    
    FRAME_WIDTH = 1
    FRAME_MARGIN = 2
    
    ICON_SIZE = 35
    ICON_BUTTON_WIDTH = 60    
    
    LABEL_SIZE_X = 174
    INPUT_SIZE_X = 100
    BUTTON_BLOCK_X = 278
    
    STEP = 0.5
    MIN_VALUE = 0.1
    MAX_VALUE = 10
    DECIMAL_COUNT = 1
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()       
    
    def initUI(self):
        self.resize(TimeInputLine.WIDTH + TimeInputLine.FRAME_MARGIN*2, TimeInputLine.HEIGHT + TimeInputLine.FRAME_MARGIN*2)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(TimeInputLine.FRAME_WIDTH)
        
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
        self.label.resize(TimeInputLine.LABEL_SIZE_X, TimeInputLine.HEIGHT)
        self.label.move(TimeInputLine.FRAME_MARGIN, TimeInputLine.FRAME_MARGIN)
        self.label.setStyleSheet(component_stylesheet)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.show()       
        
        self.spinbox = QDoubleSpinBox(self)
        self.spinbox.setRange(TimeInputLine.MIN_VALUE, TimeInputLine.MAX_VALUE)
        self.spinbox.setValue(TimeInputLine.STEP)
        self.spinbox.setSingleStep(TimeInputLine.STEP)
        self.spinbox.setDecimals(TimeInputLine.DECIMAL_COUNT)
        self.spinbox.resize(TimeInputLine.INPUT_SIZE_X, TimeInputLine.HEIGHT)
        self.spinbox.move(TimeInputLine.LABEL_SIZE_X + TimeInputLine.FRAME_MARGIN, TimeInputLine.FRAME_MARGIN)
        self.spinbox.setStyleSheet(component_stylesheet)
        self.spinbox.show()
        
        self.enter = QPushButton("", self)
        self.enter.setIcon(assets.enter)
        self.enter.setIconSize(QSize(TimeInputLine.ICON_SIZE, TimeInputLine.ICON_SIZE))
        self.enter.resize(TimeInputLine.ICON_BUTTON_WIDTH, TimeInputLine.HEIGHT)
        self.enter.move(TimeInputLine.BUTTON_BLOCK_X, TimeInputLine.FRAME_MARGIN)  
        self.enter.setStyleSheet(component_stylesheet)
        self.enter.show()
        
        self.cancel = QPushButton("", self)
        self.cancel.setIcon(assets.exit)
        self.cancel.setIconSize(QSize(TimeInputLine.ICON_SIZE, TimeInputLine.ICON_SIZE))
        self.cancel.resize(TimeInputLine.ICON_BUTTON_WIDTH, TimeInputLine.HEIGHT)
        self.cancel.move(TimeInputLine.BUTTON_BLOCK_X + TimeInputLine.ICON_BUTTON_WIDTH, TimeInputLine.FRAME_MARGIN)     
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
    
    WIDTH = 140
    HEIGHT = 45
    
    TIMER_STEP = 25
    
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
        self.time.resize(Clock.WIDTH, Clock.HEIGHT)
        self.time.setStyleSheet(clock_stylesheet)
        self.time.setAlignment(Qt.AlignHCenter)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)        
        self.timer.task = None
        
    def startClock(self):
        self.timer.start(Clock.TIMER_STEP)
        
    def stopClock(self):
        self.timer.stop()
    
    def reset(self):
        self.accumulator = 0
        self.time.setText("0:00.0")
    
    def updateTime(self):
        self.accumulator = self.accumulator + Clock.TIMER_STEP/100
        self.time.setText(str(int(self.accumulator%6000/600)) +":"+str(int(self.accumulator%600/100))+str(int(self.accumulator%100/10))+"."+str(int(self.accumulator)%10))
        if self.task != None:
            self.task()
               
