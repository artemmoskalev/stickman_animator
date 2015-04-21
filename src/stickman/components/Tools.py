'''
Created on Apr 21, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QLabel, QLineEdit, QWidget, QTimer
from PyQt5.QtCore import Qt

"""
    ---------------------------------------

    class which holds the references to the tool sets in order to switch them. can define their position and hide/show the tools
    
    ---------------------------------------

"""
class ToolSet():
    
    def __init__(self, parent):
        self.stickman_tools = StickmanTools(parent)
        self.animation_tools = AnimationTools(parent)
        self.io_tools = IOTools(parent)
        self.other_tools = OtherTools(parent)
        self.hide()
        
    def move(self, x, y):
        self.stickman_tools.move(x, y)
        self.animation_tools.move(x, y)
        self.io_tools.move(x, y)
        self.other_tools.move(x, y)
                
    def showStickmanTools(self):        
        self.hide()        
        self.stickman_tools.show()
        self.stickman_tools.showButtons()
        
    def showAnimationTools(self):
        self.hide()
        self.animation_tools.show()
        
    def showIOTools(self):
        self.hide()
        self.io_tools.show()
                
    def showOtherTools(self):
        self.hide()
        self.other_tools.show()
        
    def hide(self):
        self.stickman_tools.hide()
        self.animation_tools.hide()
        self.io_tools.hide()
        self.other_tools.hide()   
    
"""
    ---------------------------------------

    CLASSES WHICH REPRESENT STICKMAN TOOLS
    
    ---------------------------------------

"""

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR CREATION AND DELETION OF STICKMEN
    
    ---------------------------------------

"""
class StickmanTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(304, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                            """
                        
        self.create_stickman = QPushButton('Create Stickman', self)
        self.create_stickman.resize(150, 30)
        self.create_stickman.move(2, 2)        
        self.create_stickman.setStyleSheet(button_stylesheet)
        self.create_stickman.clicked.connect(self.showDialog)
        
        self.delete_stickman = QPushButton('Delete Stickman', self)
        self.delete_stickman.resize(150, 30)
        self.delete_stickman.move(152, 2)        
        self.delete_stickman.setStyleSheet(button_stylesheet)
        self.delete_stickman.clicked.connect(self.showDialog)
    
        self.input = InputLine(self)        
        self.input.addOkListener(self.showButtons)
        self.input.addOkListener(self.readText)
        self.input.addCancelListener(self.showButtons)
        self.input.move(0, 2)
        self.input.hide()
    
    """ Method which shows the input line and hides buttons """
    def showDialog(self):
        if self.sender() == self.create_stickman:
            self.input.setLabelText("Enter New StickName: ")            
        else:
            self.input.setLabelText("Enter Name To Delete: ")  
        self.resize(587, 34)
        self.create_stickman.hide()
        self.delete_stickman.hide()
        self.input.show()
    
    """ Listener to take actions when ok button was pressed and input text has been read"""
    def readText(self):
        if self.input.getLabelText() == "Enter New StickName: ":
            print("New Stickman " + self.input.getText() + " was created!")
        else:
            print("The Stickman " + self.input.getText() + " was removed!!")
    
    """ Listener to close the input line and show buttons again """  
    def showButtons(self):
        self.resize(304, 34)
        self.create_stickman.show()
        self.delete_stickman.show()
        self.input.hide()
            
            
"""
    ---------------------------------------

    ClASS RESPONSIBLE ANIMATION OF STICKMEN
    
    ---------------------------------------

""" 
class AnimationTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(154, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                            """
                        
        self.start_animation = QPushButton('Start Animation', self)
        self.start_animation.resize(150, 30)
        self.start_animation.move(2, 2)        
        self.start_animation.setStyleSheet(button_stylesheet)
        self.start_animation.clicked.connect(self.pressAnimationOnOffButton)
        self.start_animation.show()        
        
        self.stop_animation = QPushButton('End Animation', self)
        self.stop_animation.resize(150, 30)
        self.stop_animation.move(2, 2)        
        self.stop_animation.setStyleSheet(button_stylesheet)
        self.stop_animation.clicked.connect(self.pressAnimationOnOffButton)
        self.stop_animation.hide()        

        self.clock = Clock(self)
        self.clock.hide()
        self.clock.move(152, 0)

    def pressAnimationOnOffButton(self):
        if self.sender() == self.start_animation:
            self.resize(294, 34)            
            self.start_animation.hide()
            self.stop_animation.show()
            self.clock.startClock()
            self.clock.show()
        else:
            self.resize(154, 34)            
            self.stop_animation.hide()
            self.start_animation.show()
            self.clock.stopClock()
            self.clock.hide()
            
"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SAVING AND LOADING ANIMATIONS
    
    ---------------------------------------

"""       
class IOTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(304, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                            """
                        
        save_animation = QPushButton('Save Animation', self)
        save_animation.resize(150, 30)
        save_animation.move(2, 2)        
        save_animation.setStyleSheet(button_stylesheet)
       
        load_animation = QPushButton('Load Animation', self)
        load_animation.resize(150, 30)
        load_animation.move(152, 2)        
        load_animation.setStyleSheet(button_stylesheet)


"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR CHANGING BACKGROUND AND FOR OTHER ADDITIONAL FEATURES
    
    ---------------------------------------

"""
class OtherTools(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(304, 34)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        button_stylesheet = """
                                .QPushButton {
                                    font-weight: bold;
                                    font-size: 13px;
                                    background-color:#E0E0E0;
                                }
                                .QPushButton:pressed {
                                    background-color:#CCCCCC;
                                }
                            """
                        
        change_background = QPushButton('Set Background', self)
        change_background.resize(150, 30)
        change_background.move(2, 2)        
        change_background.setStyleSheet(button_stylesheet)
       
        remove_background = QPushButton('Clear Background', self)
        remove_background.resize(150, 30)
        remove_background.move(152, 2)        
        remove_background.setStyleSheet(button_stylesheet)


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
    
    def addOkListener(self, onOkEvent):
        self.ok.clicked.connect(onOkEvent)
        
    def addCancelListener(self, onCancelEvent):
        self.cancel.clicked.connect(onCancelEvent)
    
    def getText(self):
        return self.text.text()
        
    def setLabelText(self, text):
        self.label.setText(text)
        
    def getLabelText(self):
        return self.label.text()
        
class Clock(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        clock_stylesheet = """
                                .QLabel {
                                    padding-top: 4px;
                                    font-weight: bold;
                                    font-size: 20px;
                                    color:#ff5e5e;
                                }
                            """  
        
        self.accumulator = 0
        
        self.time = QLabel("0:00.0", self)
        self.time.resize(140, 30)
        self.time.setStyleSheet(clock_stylesheet)
        self.time.setAlignment(Qt.AlignHCenter)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)        
    
    def startClock(self):
        self.timer.start(100)
        print("clock started!")
        
    def stopClock(self):
        self.timer.stop()
        print("clock stopped!")
           
    def updateTime(self):
        self.accumulator = self.accumulator + 1
        self.time.setText(str(int(self.accumulator%6000/600)) +":"+str(int(self.accumulator%600/100))+str(int(self.accumulator%100/10))+"."+str(self.accumulator%10))
        
        
