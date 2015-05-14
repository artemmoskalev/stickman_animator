'''
Created on Apr 25, 2015

@author: Artem
'''

from PyQt5.Qt import QPushButton, QFrame, QSize, QRect, QFileDialog

from stickman.tools.Components import Clock, TimeInputLine
from stickman.model.World import getWorld
from stickman.UI.AssetManager import assets
from stickman.tools.XMLAdapter import XML

import math

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
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setFrameRect(QRect(290, 0, 404, 49))
               
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
                       
        self.save_animation = QPushButton('Save Animation', self)
        self.save_animation.resize(200, 45)
        self.save_animation.move(292, 2)        
        self.save_animation.setStyleSheet(button_stylesheet)
        self.save_animation.clicked.connect(self.saveXML)
       
        self.load_animation = QPushButton('Load Animation', self)
        self.load_animation.resize(200, 45)
        self.load_animation.move(492, 2)        
        self.load_animation.setStyleSheet(button_stylesheet)
        self.load_animation.clicked.connect(self.fromXML)
        
        self.player = AnimationPlayer(self)
        self.player.move(0, 2)
        self.player.show()
        
        self.time_input = TimeInputLine(self)
        self.time_input.move(698, 1)
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
    
    def hideAll(self):
        self.delete_button.hide()
        self.time_button.hide()
        self.copy_button.hide()
        self.time_input.hide()
        self.save_animation.hide()
        self.load_animation.hide()
        self.setFrameShape(QFrame.NoFrame)
    def showAll(self):
        self.showButtonBlock()
        self.save_animation.show()
        self.load_animation.show()
        self.setFrameShape(QFrame.StyledPanel)
    
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
       
    """ listeners for XML binding and parsing """
    def saveXML(self):
        if len(self.tools.framemenu.getAllFrames()) > 1:
            result = QFileDialog.getSaveFileName(self, 'Choose the destination for the animation file!', '.', 'Animation File (*.armo)')
            if result[0] != "":
                XML().toXML(self.tools.framemenu.getAllFrames(), result[0])
        
    def fromXML(self):
        file = QFileDialog.getOpenFileName(self, "Load Animation", ".", "Animation Files (*.armo)")
        if file[0] != "":
            frames = XML().fromXML(self.tools.framemenu.getAllFrames(), file[0])
            
            self.tools.framemenu.removeAllFrames()
            for frame in frames:
                self.tools.framemenu.addNewFrame(frame)
            if len(frames) > 0:
                getWorld().setWorldFrom(frames[0])
        
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
        self.steps = 0          #number of intermediate steps between two frames
        self.step_counter = 0   #number of steps already taken for the interpolation
    
    """ called when the play button is pressed """      
    def onPlay(self):        
        self.disable()
        self.clock.show()
        self.stop_button.show()
        if self.playing == AnimationPlayer.STOPPED: #starting
            self.play_button.setIcon(assets.pause) 
            self.playing = AnimationPlayer.PLAYING                        
            self.play()
        elif self.playing == AnimationPlayer.PAUSED:
            self.play_button.setIcon(assets.pause) 
            self.playing = AnimationPlayer.PLAYING                        
            self.clock.startClock()
        else:                                       #pausing
            self.play_button.setIcon(assets.play) 
            self.playing = AnimationPlayer.PAUSED 
            self.clock.stopClock()        
            
    """ called when the stop button is pressed or the animation is over """                          
    def onStop(self):
        if not self.playing == AnimationPlayer.STOPPED:
            self.enable()
            self.play_button.setIcon(assets.play) 
            self.playing = AnimationPlayer.STOPPED              
            self.clock.stopClock()
            self.clock.reset()
            self.clock.hide()
            self.stop_button.hide()  
    
    """ Methods which enable and disable screen controls while the animation plays """
    def disable(self):
        self.parent().parent().control_panel.setEnabled(False)
        self.parent().parent().canvas.setEnabled(False)
        self.parent().tools.framemenu.hide()
        self.parent().hideAll()
        
    def enable(self):
        self.parent().parent().control_panel.setEnabled(True)
        self.parent().parent().canvas.setEnabled(True)
        self.parent().tools.framemenu.show()
        self.parent().showAll()
    
    """ Entry method for the animation """
    def play(self):
        if self.parent().tools.framemenu.getActiveFrame() == None:
            self.next_frame = self.parent().tools.framemenu.getFirstFrame()
        else:
            self.next_frame = self.parent().tools.framemenu.getActiveFrame()[1]
        if self.next_frame != None:
            self.reloadFrames()
        else:
            self.onStop()
            
    """ this method loads two frames between which it is required to interpolate.
        It loads frames from the FrameList until there are no more pairs of frames """
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
            self.onStop()
    
    """ Methods used to perform the interpolation job as they are """
    def updateAnimation(self):
        if self.step_counter < self.steps:
            self.step_counter = self.step_counter + 1            
            step_ratio = self.step_counter/self.steps            
            # interpolate all stickmen one by one
            for stickman in self.old_frame.stickmen:                
                new_stickman = self.next_frame.getStickman(stickman.name)                
                # need to check the new stickman, because it can be removed in the next frame
                if new_stickman != None:
                    self.interpolatePosition(stickman, new_stickman, step_ratio)
                    self.interpolateJoints(stickman, new_stickman, step_ratio)        
        else:
            self.reloadFrames()    # called when two frames have interpolated enough to swap the last approximation for the real next frame
    
    """ Interpolates between the positions of stickman body """
    def interpolatePosition(self, old_stickman, new_stickman, ratio):
        x_difference = new_stickman.x - old_stickman.x
        y_difference = new_stickman.y - old_stickman.y
        current_x = x_difference*ratio
        current_y = y_difference*ratio
                    
        modified_stickman = self.current_frame.getStickman(old_stickman.name)
        modified_stickman.x = old_stickman.x + current_x
        modified_stickman.y = old_stickman.y + current_y
    
    """ Interpolates between the positions of stickman joints """
    def interpolateJoints(self, old_stickman, new_stickman, ratio):
        i = 0
        while i < len(old_stickman.joints):
            old_joint = old_stickman.joints[i]
            new_joint = new_stickman.joints[i]                       
                        
            if (old_joint.attachment != None and new_joint.attachment != None):
                # degree difference and its alternatives are used to calculate the shortes path in rotation between two points of stickman
                degree_difference = new_joint.angle - old_joint.angle
                degree_difference_alternative = (2*math.pi - old_joint.angle + new_joint.angle)
                if abs(degree_difference) <= abs(degree_difference_alternative):
                    current_degree_change = degree_difference*ratio
                else:
                    current_degree_change = degree_difference_alternative*ratio
                
                modified_stickman = self.current_frame.getStickman(old_stickman.name)
                degree_by = old_joint.angle + current_degree_change - modified_stickman.joints[i].angle                        
                modified_stickman.joints[i].rotateBy(degree_by)                
            i = i + 1  
    
    