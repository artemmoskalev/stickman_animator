'''
Created on Apr 25, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QIcon, QSize, QDoubleSpinBox, QLabel
from PyQt5.QtCore import Qt
from stickman.tools.Components import Clock

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SAVING AND LOADING ANIMATIONS, AND THEIR MANIPULATIONS
    
    ---------------------------------------

"""       
class AnimationToolsPanel(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.resize(1100, 49)
        #self.setFrameStyle(QFrame.StyledPanel)
        #self.setFrameRect(QRect(0, 0, 304, 34))
        #self.setLineWidth(1)
        
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
        """                
        self.save_animation = QPushButton('Save Animation', self)
        self.save_animation.resize(150, 30)
        self.save_animation.move(2, 2)        
        self.save_animation.setStyleSheet(button_stylesheet)
       
        self.load_animation = QPushButton('Load Animation', self)
        self.load_animation.resize(150, 30)
        self.load_animation.move(152, 2)        
        self.load_animation.setStyleSheet(button_stylesheet)
        """
                 
        self.player = AnimationPlayer(self)
        self.player.move(0, 2)
        self.player.show()
        
        self.time_input = TimeInputLine(self)
        self.time_input.move(698, 2)
        self.time_input.hide()       
        
        self.time_button = QPushButton('', self)
        self.time_button.setIcon(QIcon("resources/time.png"))
        self.time_button.setIconSize(QSize(35, 35))
        self.time_button.resize(60, 45)
        self.time_button.move(918, 2)        
        self.time_button.setStyleSheet(button_stylesheet)
        self.time_button.clicked.connect(self.timeFrameListener)
        self.time_button.show()        

        self.copy_button = QPushButton('', self)
        self.copy_button.setIcon(QIcon("resources/copy.png"))
        self.copy_button.setIconSize(QSize(35, 35))
        self.copy_button.resize(60, 45)
        self.copy_button.move(978, 2)        
        self.copy_button.setStyleSheet(button_stylesheet)
        self.copy_button.clicked.connect(self.copyFrameListener)
        self.copy_button.show() 
        
        self.delete_button = QPushButton('', self)
        self.delete_button.setIcon(QIcon("resources/delete.png"))
        self.delete_button.setIconSize(QSize(35, 35))
        self.delete_button.resize(60, 45)
        self.delete_button.move(1038, 2)        
        self.delete_button.setStyleSheet(button_stylesheet)
        self.delete_button.clicked.connect(self.deleteListener)
        self.delete_button.show() 
    
    """ Methods to show/hide the input time and frame-control buttons """
    def showButtonBlock(self):
        self.delete_button.show()
        self.time_button.show()
        self.copy_button.show()
        self.time_input.hide()
    def showInputTime(self):
        self.delete_button.hide()
        self.time_button.hide()
        self.copy_button.hide()  
        self.time_input.label.setText(self.parent().canvas.framemenu.getActiveFrame().text().split(":")[0] + ":")
        self.time_input.show()
    
    """ Listeners for delete, copy and time buttons """
    def deleteListener(self):
        self.parent().canvas.framemenu.deleteFrame(self)
    def copyFrameListener(self):
        self.parent().canvas.framemenu.copyFrame()
    def timeFrameListener(self):    
        active_frame = self.parent().canvas.framemenu.getActiveFrame()
        if not active_frame == None:
            self.showInputTime()  
            
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
        self.enter.setIcon(QIcon("resources/enter.png"))
        self.enter.setIconSize(QSize(35, 35))
        self.enter.resize(60, 43)
        self.enter.move(278, 2)  
        self.enter.setStyleSheet(component_stylesheet)  
        self.enter.clicked.connect(self.onAcceptListener)  
        self.enter.show()
        
        self.cancel = QPushButton("", self)
        self.cancel.setIcon(QIcon("resources/exit.png"))
        self.cancel.setIconSize(QSize(35, 35))
        self.cancel.resize(60, 43)
        self.cancel.move(338, 2)     
        self.cancel.setStyleSheet(component_stylesheet) 
        self.cancel.clicked.connect(self.onCancelListener)
        self.cancel.show()
    
    """ button listeners """
    def onCancelListener(self):
        self.parent().showButtonBlock()
    
    def onAcceptListener(self):
        time = self.spinbox.value()
        self.parent().parent().canvas.framemenu.changeFrameTime(time)
        self.parent().showButtonBlock()
    
"""
    -------------------------------
        CLASS WHICH PLAYS THE ANIMATION AND COMBINES FRAMES INTO ONE FILM
    -------------------------------
"""
class AnimationPlayer(QFrame):
    
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2 
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()  
    
    def initUI(self):
        self.resize(260, 45)
        self.playing = AnimationPlayer.STOPPED
        
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
        
        self.play_button = QPushButton('', self)
        self.play_button.setIcon(QIcon("resources/play.png"))
        self.play_button.setIconSize(QSize(35, 35))
        self.play_button.resize(60, 45)
        self.play_button.move(0, 0)        
        self.play_button.setStyleSheet(button_stylesheet)
        self.play_button.clicked.connect(self.onPlay)
        self.play_button.show()        
        
        self.clock = Clock(self)
        self.clock.move(60, 0)
        self.clock.hide()
        
        self.stop_button = QPushButton('', self)
        self.stop_button.setIcon(QIcon("resources/stop.png"))
        self.stop_button.setIconSize(QSize(35, 35))
        self.stop_button.resize(60, 45)
        self.stop_button.move(200, 0)        
        self.stop_button.setStyleSheet(button_stylesheet)
        self.stop_button.clicked.connect(self.onStop)
        self.stop_button.hide() 
    
    def onPlay(self):
        if not self.playing == AnimationPlayer.PLAYING: #starting
            self.play_button.setIcon(QIcon("resources/pause.png")) 
            self.playing = AnimationPlayer.PLAYING
            self.clock.startClock()
        else:                                       #pausing
            self.play_button.setIcon(QIcon("resources/play.png")) 
            self.playing = AnimationPlayer.PAUSED 
            self.clock.stopClock()
        self.clock.show()
        self.stop_button.show()
                               
    def onStop(self):
        if not self.playing == AnimationPlayer.STOPPED:
            self.play_button.setIcon(QIcon("resources/play.png")) 
            self.playing = AnimationPlayer.STOPPED  
            self.clock.hide()
            self.clock.reset()
            self.stop_button.hide()  
    
    def play(self):
        pass            
    def stop(self):
        pass
    def pause(self):
        pass
    def playFrom(self, frame):
        pass