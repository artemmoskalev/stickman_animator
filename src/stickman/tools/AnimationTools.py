'''
Created on Apr 25, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QSize

from stickman.tools.Components import Clock, TimeInputLine
from stickman.model.World import getWorld
from stickman.UI.AssetManager import assets

import copy

"""
    ---------------------------------------

    ClASS RESPONSIBLE FOR SAVING AND LOADING ANIMATIONS, AND THEIR MANIPULATIONS
    
    ---------------------------------------

"""       
class AnimationToolsPanel(QFrame):
    
    def __init__(self, parent, tools):
        super().__init__(parent)
        self.tools = tools
        self.initUI()
        
    def initUI(self):
        self.resize(1100, 49)
               
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
        self.time_input.addAcceptListener(self.onAcceptListener)
        self.time_input.addCancelListener(self.onCancelListener)
        self.time_input.hide()       
        
        self.time_button = QPushButton('', self)
        self.time_button.setIcon(assets.time)
        self.time_button.setIconSize(QSize(35, 35))
        self.time_button.resize(60, 45)
        self.time_button.move(918, 2)        
        self.time_button.setStyleSheet(button_stylesheet)
        self.time_button.clicked.connect(self.timeFrameListener)
        self.time_button.show()        

        self.copy_button = QPushButton('', self)
        self.copy_button.setIcon(assets.copy)
        self.copy_button.setIconSize(QSize(35, 35))
        self.copy_button.resize(60, 45)
        self.copy_button.move(978, 2)        
        self.copy_button.setStyleSheet(button_stylesheet)
        self.copy_button.clicked.connect(self.copyFrameListener)
        self.copy_button.show() 
        
        self.delete_button = QPushButton('', self)
        self.delete_button.setIcon(assets.delete)
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
        self.time_input.label.setText(self.tools.framemenu.getActiveFrame()[0].text().split(":")[0] + ":")
        self.time_input.show()
    
    
    """ time change listeners, which are called by the TimeInput component """
    def onCancelListener(self):
        self.showButtonBlock()    
    def onAcceptListener(self):
        time = self.time_input.spinbox.value()
        self.tools.framemenu.changeFrameTime(time)
        self.showButtonBlock()
    
    """ Listeners for delete, copy and time buttons """
    def deleteListener(self):
        self.tools.framemenu.deleteFrame(self)
    def copyFrameListener(self):
        self.tools.framemenu.copyFrame()
    def timeFrameListener(self):    
        active_frame = self.tools.framemenu.getActiveFrame()
        if not active_frame == None:
            self.showInputTime()  
       

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
        self.play_button.setIcon(assets.play)
        self.play_button.setIconSize(QSize(35, 35))
        self.play_button.resize(60, 45)
        self.play_button.move(0, 0)        
        self.play_button.setStyleSheet(button_stylesheet)
        self.play_button.clicked.connect(self.onPlay)
        self.play_button.show()        
        
        self.clock = Clock(self)
        self.clock.move(60, 0)
        self.clock.task = self.updateAnimation
        self.clock.hide()
        
        self.stop_button = QPushButton('', self)
        self.stop_button.setIcon(assets.stop)
        self.stop_button.setIconSize(QSize(35, 35))
        self.stop_button.resize(60, 45)
        self.stop_button.move(200, 0)        
        self.stop_button.setStyleSheet(button_stylesheet)
        self.stop_button.clicked.connect(self.onStop)
        self.stop_button.hide() 
        
        self.old_frame = None
        self.current_frame = None  
        self.next_frame = None       
        self.steps = 0
        self.step_counter = 0
                
    def onPlay(self):
        if not self.playing == AnimationPlayer.PLAYING: #starting
            self.play_button.setIcon(assets.pause) 
            self.playing = AnimationPlayer.PLAYING                        
            self.play()
        else:                                       #pausing
            self.play_button.setIcon(assets.play) 
            self.playing = AnimationPlayer.PAUSED 
            self.clock.stopClock()
        self.clock.show()
        self.stop_button.show()
                               
    def onStop(self):
        if not self.playing == AnimationPlayer.STOPPED:
            self.play_button.setIcon(assets.play) 
            self.playing = AnimationPlayer.STOPPED  
            self.clock.hide()
            self.clock.reset()
            self.stop_button.hide()  
    
    """ this method loads two frames between which it is required to interpolate """
    def reloadFrames(self):
        self.clock.stopClock()
        
        self.old_frame = self.next_frame        
        self.current_frame = self.old_frame.copy()
        getWorld().setWorldFrom(self.current_frame)
        
        self.next_frame = self.parent().tools.framemenu.getNextFrame(self.old_frame)
        if self.next_frame != None:            
            self.steps = (self.next_frame.time*1000)/25
            self.step_counter = 0
            self.clock.startClock()
        else:
            print("Animation Over!")
            self.clock.stopClock()
    
    def updateAnimation(self):
        if self.step_counter < self.steps:
            self.step_counter = self.step_counter + 1
            
            step_ratio = self.step_counter/self.steps
            
            for stickman in self.old_frame.stickmen:                
                new_stickman = self.next_frame.getStickman(stickman.name)
                
                if new_stickman != None:
                    x_difference = new_stickman.x - stickman.x
                    y_difference = new_stickman.y - stickman.y
                    current_x = x_difference*step_ratio
                    current_y = y_difference*step_ratio
                    
                    modified_stickman = self.current_frame.getStickman(stickman.name)
                    modified_stickman.x = stickman.x + current_x
                    modified_stickman.y = stickman.y + current_y
                    
                    i = 0
                    while i < len(stickman.joints):
                        old_joint = stickman.joints[i]
                        new_joint = new_stickman.joints[i]                       
                        
                        if (old_joint.angle != None and new_joint.angle != None):
                            degree_difference = new_joint.angle - old_joint.angle
                            current_degree = degree_difference*step_ratio
                            
                            degree_by = old_joint.angle + current_degree - modified_stickman.joints[i].angle                        
                            modified_stickman.joints[i].rotateBy(degree_by)
                        i = i + 1                        
                    
        else:
            self.reloadFrames()
    
    def play(self):
        self.next_frame = self.parent().tools.framemenu.getFirstFrame()
        if self.next_frame != None:
            self.reloadFrames()            
        
    def stop(self):
        self.animation_timer.stop()
        
    def pause(self):
        pass
    def playFrom(self, frame):
        pass