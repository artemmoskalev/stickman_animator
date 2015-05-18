'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPen, QRectF, QFont, QFontMetrics, QImage
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QLine

from stickman.tools.Components import Frame
import math
import copy

from stickman.UI.AssetManager import assets

class Stickman():
    
    ARM_LENGTH = 80
    HAND_LENGTH = 90
    LEG_LENGTH = 95
    TOE_LENGTH = 30
    STICK_WIDTH = 5
    
    HEAD_CLICK_RATIO = 3/4
    
    def __init__(self, name, x, y):
        self.name = name        
        self.x = x
        self.y = y
        self.initBody()
        
    def moveTo(self, x, y):
        if x > - Head.HEAD_RADIUS*Stickman.HEAD_CLICK_RATIO and x < World.WIDTH + Head.HEAD_RADIUS*Stickman.HEAD_CLICK_RATIO:
            self.x = x
        if y > - Head.HEAD_RADIUS*Stickman.HEAD_CLICK_RATIO and y < World.HEIGHT + Head.HEAD_RADIUS*Stickman.HEAD_CLICK_RATIO:
            self.y = y
    
    def initBody(self):
        self.head = Head(self)
        self.words = Words(self)
        self.spine = Spine(self)
        self.joints = list()       
        
        """ CREATING LEFT LEG """
        left_leg_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.SPINE_LENGTH)        
        left_knee = left_leg_attachment.createNextJoint(True, Stickman.LEG_LENGTH, 25)        
        left_foot = left_knee.createNextJoint(True, Stickman.LEG_LENGTH, 0)        
        left_toe = left_foot.createNextJoint(False, Stickman.TOE_LENGTH, 90)
        
        self.joints.append(left_leg_attachment)
        self.joints.append(left_knee)
        self.joints.append(left_foot)
        self.joints.append(left_toe)
        
        """ CREATING RIGHT LEG """
        right_leg_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.SPINE_LENGTH)        
        right_knee = right_leg_attachment.createNextJoint(True, Stickman.LEG_LENGTH, -25)        
        right_foot = right_knee.createNextJoint(True, Stickman.LEG_LENGTH, 0)       
        right_toe = right_foot.createNextJoint(False, Stickman.TOE_LENGTH, -90)
        
        self.joints.append(right_leg_attachment)
        self.joints.append(right_knee)
        self.joints.append(right_foot)
        self.joints.append(right_toe)
        
        """ CREATING LEFT ARM """
        left_arm_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.NECK_LENGTH)        
        left_elbow = left_arm_attachment.createNextJoint(True, Stickman.ARM_LENGTH, 55)        
        left_hand = left_elbow.createNextJoint(True, Stickman.HAND_LENGTH, 135)
        
        self.joints.append(left_arm_attachment)
        self.joints.append(left_elbow)
        self.joints.append(left_hand)
        
        """ CREATING RIGHT ARM """
        right_arm_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.NECK_LENGTH)        
        right_elbow = right_arm_attachment.createNextJoint(True, Stickman.ARM_LENGTH, -45)                
        right_hand = right_elbow.createNextJoint(True, Stickman.HAND_LENGTH, -35)
        
        self.joints.append(right_arm_attachment)
        self.joints.append(right_elbow)
        self.joints.append(right_hand)
        
    def setHappy(self):
        self.head.expression.setExpression(Expression.SMILE)
    def setSad(self):
        self.head.expression.setExpression(Expression.SAD)
    def setConfused(self):
        self.head.expression.setExpression(Expression.CONFUSED)
        
    def sayLeft(self, text):
        self.words.setText(text, Words.LEFT)
    def sayRight(self, text):
        self.words.setText(text, Words.RIGHT)
    def sayRemove(self):
        self.words.setText("", Words.NONE)
        
    def draw(self, painter):
        self.head.draw(painter)
        self.spine.draw(painter)
             
        # draw joints themselves
        # only the root nodes in the hierarchy need to be called. Thats why only draw all method is called
        # Dependent nodes` paint method will be called revursively itself
        for joint in self.joints:
            if joint.attachment == None:
                joint.draw(painter)      
        
        self.words.draw(painter)
                
    """ called from the World when click is detected. Bodyparts of stickmen are to decide themselves if they have been clicked 
        Processes the event only in case it has not been used by some other stickman """
    def mousePressed(self, event):
        if not event.isProcessed:
            for joint in reversed(self.joints):
                joint.mousePressed(event)
            self.head.mousePressed(event)
               
    def mouseReleased(self, event):
        if not event.isProcessed:
            for joint in reversed(self.joints):
                joint.mouseReleased(event)
            self.head.mouseReleased(event)
        
    def mouseMoved(self, event):
        if not event.isProcessed:
            for joint in reversed(self.joints):
                joint.mouseMoved(event)
            self.head.mouseMoved(event)

class Head():
    
    HEAD_RADIUS = 50
    HEAD_ARC = 16*360
    
    def __init__(self, body):
        self.body = body
        self.expression = Expression(body)
        self.dragged = False
    
    def draw(self, painter):
        painter.setPen(QPen(Qt.black, Stickman.STICK_WIDTH, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        
        painter.drawArc(QRectF(self.body.x-Head.HEAD_RADIUS, self.body.y-Head.HEAD_RADIUS, Head.HEAD_RADIUS*2, Head.HEAD_RADIUS*2), 0, Head.HEAD_ARC) 
        painter.drawEllipse(QRectF(self.body.x-Head.HEAD_RADIUS, self.body.y-Head.HEAD_RADIUS, Head.HEAD_RADIUS*2, Head.HEAD_RADIUS*2))        
        self.expression.draw(painter)
    
    """ head click and move listeners """
    def mousePressed(self, event):
        if not event.isProcessed:
            distance = math.sqrt((self.body.x-event.x)**2+(self.body.y-event.y)**2)
            if distance <= Head.HEAD_RADIUS:
                self.dragged = True
                getWorld().setActive(self.body.name)
                event.process()
           
    def mouseReleased(self, event):
        self.dragged = False
        
    def mouseMoved(self, event):
        if self.dragged:
            self.body.moveTo(event.x, event.y)

class Expression():
    
    SMILE_WIDTH = 70
    EYE_WIDTH = 15
    
    SMILE = 1
    SAD = 2
    CONFUSED = 3
    
    """ these are relative to body coordinates """
    LEFT_EYE_X = -30
    RIGHT_EYE_X = 15
    EYE_Y = -25
    
    """ define the arc lengths of circles which are drawn """
    SMILE_ARC_START = 9*360 
    SMILE_ARC = 6*360    
    SAD_ARC_START = 1.5*360
    SAD_ARC = 5*360
    O_ARC = 16*360
    
    def __init__(self, body):
        self.body = body
        self.expression = Expression.SMILE
    
    def draw(self, painter):        
        painter.setBrush(QBrush(Qt.SolidPattern))
        
        painter.drawEllipse(QRectF(self.body.x + Expression.LEFT_EYE_X, self.body.y + Expression.EYE_Y, Expression.EYE_WIDTH, Expression.EYE_WIDTH))
        painter.drawEllipse(QRectF(self.body.x + Expression.RIGHT_EYE_X, self.body.y + Expression.EYE_Y, Expression.EYE_WIDTH, Expression.EYE_WIDTH))        
        
        if self.expression == Expression.SMILE:
            self.drawSmile(painter)
        elif self.expression == Expression.SAD:
            self.drawSad(painter)
        else:
            self.drawConfused(painter)        
    
    def setExpression(self, expression):
        self.expression = expression
    
    def drawSmile(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/2, self.body.y-Expression.SMILE_WIDTH/2, Expression.SMILE_WIDTH, Expression.SMILE_WIDTH), 
                        Expression.SMILE_ARC_START, Expression.SMILE_ARC)
    def drawSad(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/2, self.body.y+Expression.SMILE_WIDTH/7, Expression.SMILE_WIDTH, Expression.SMILE_WIDTH), 
                        Expression.SAD_ARC_START, Expression.SAD_ARC)
    def drawConfused(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/3.4, self.body.y, Expression.SMILE_WIDTH/1.7, Expression.SMILE_WIDTH/2), 0, Expression.O_ARC)

class Words():
        
    WORDS_WIDTH = 300
    WORDS_HEIGHT = 80
    TEXT_PADDING = 15
    
    NONE = 0
    LEFT = 1
    RIGHT = 2
    
    FONT_SIZE = 16
    PEN_SIZE = 2
    
    MAXIMUM_TEXT_WIDTH = 448
    
    def __init__(self, body):
        self.body = body
        self.text = "..."
        self.side = Words.NONE
        
    def setText(self, text, side):
        if len(text) != 0:
            self.text = text
        else:
            self.text = "..."
        self.side = side
            
    def draw(self, painter):
        font = QFont(QFont("Times", Words.FONT_SIZE, QFont.Bold))    
        self.formatText(font)
        
        if self.side == Words.RIGHT:
            painter.drawPixmap(self.body.x + Head.HEAD_RADIUS/2, self.body.y + Head.HEAD_RADIUS/4, 
                                Words.WORDS_WIDTH, Words.WORDS_HEIGHT, assets.speak_right)
                
            painter.setPen(QPen(Qt.black, Words.PEN_SIZE, Qt.SolidLine))
            painter.setFont(font)            
            painter.drawText(QRectF(self.body.x + Head.HEAD_RADIUS/2 + Words.TEXT_PADDING*4, self.body.y + Words.TEXT_PADDING*1.7, 
                                    Words.WORDS_WIDTH - Words.TEXT_PADDING*5, Words.WORDS_HEIGHT - Words.TEXT_PADDING*2), 
                             Qt.AlignCenter | Qt.TextWrapAnywhere, self.text) 
                
        elif self.side == Words.LEFT:
            painter.drawPixmap(self.body.x - Head.HEAD_RADIUS/2 - Words.WORDS_WIDTH, self.body.y + Head.HEAD_RADIUS/4, 
                                Words.WORDS_WIDTH, Words.WORDS_HEIGHT, assets.speak_left)                     
                            
            painter.setPen(QPen(Qt.black, Words.PEN_SIZE, Qt.SolidLine))
            painter.setFont(font)
            painter.drawText(QRectF(self.body.x - Head.HEAD_RADIUS/2 - Words.WORDS_WIDTH + Words.TEXT_PADDING, self.body.y + Words.TEXT_PADDING*1.7, 
                                    Words.WORDS_WIDTH - Words.TEXT_PADDING*5, Words.WORDS_HEIGHT - Words.TEXT_PADDING*2), 
                             Qt.AlignCenter | Qt.TextWrapAnywhere, self.text) 
                
    def formatText(self, font):
        metrics = QFontMetrics(font)
        width = metrics.width(self.text)
        
        need_to_modify = False
        
        while(width > Words.MAXIMUM_TEXT_WIDTH):
            need_to_modify = True
            self.text = self.text[0:-1]
            width = metrics.width(self.text)
        
        if need_to_modify:
            self.text = self.text[0:-3]
            self.text = self.text + "..."
           
class Spine():
    
    NECK_LENGTH = 40
    SPINE_LENGTH = 180
    
    def __init__(self, body):
        self.body = body
    
    def draw(self, painter):
        painter.setPen(QPen(Qt.black, Stickman.STICK_WIDTH, Qt.SolidLine))        
        painter.drawLine(QLine(self.body.x, self.body.y+Head.HEAD_RADIUS, self.body.x, self.body.y+Head.HEAD_RADIUS+Spine.SPINE_LENGTH))

class Joint():
    
    JOINT_RADIUS = 10
    
    PEN_WIDTH = 2
    ARC_LENGTH = 16*360
    
    """ initialize the joint. The position of the joint is relative to the stickman`s head center """
    def __init__(self, body, isActive, relative_x, relative_y):        
        self.body = body
        self.isActive = isActive
        self.x = relative_x
        self.y = relative_y
        self.next = None  #next is another joint which is dependent on this one
        #information about the previous joint
        self.attachment = None  #attachment is another joint which this joint is dependent on    
        self.length = None      #distance to the previous attachment
        self.angle = None       #degree in rad to the previous attachment
        self.dragged = False
    
    """ calculate the relative coordinates of the new joints using the given length and degrees of rotation from the current joint.
        Degree parameter is in 1/360th degrees.
        Returns the next joint object. """
    def createNextJoint(self, isActive, length, degree):
        degree_rad = math.radians(degree)
        relative_x = math.sin(degree_rad)*length
        relative_y = math.cos(degree_rad)*length
        #these lines create a new joint and bind two joints together with one-to-one relationship
        new_joint = Joint(self.body, isActive, self.x-relative_x, self.y+relative_y)
        self.next = new_joint
        new_joint.setAttachment(self, length, degree_rad)
        return new_joint
    
    """ Setters for specifying dependency of joints """
    def setAttachment(self, joint, length, degree):
        self.attachment = joint
        self.length = length
        self.angle = degree
    
    def draw(self, painter):   
        #first draw the limb to hide it under the joint
        if self.next != None:            
            painter.setPen(QPen(Qt.black, Stickman.STICK_WIDTH, Qt.SolidLine))        
            painter.drawLine(QLine(self.body.x + self.next.x, self.body.y + self.next.y, self.body.x + self.x, self.body.y + self.y))     
        if self.isActive:
            center_x = self.body.x + self.x
            center_y = self.body.y + self.y
            painter.setPen(QPen(Qt.black, Joint.PEN_WIDTH, Qt.SolidLine))
            painter.drawArc(QRectF(center_x - Joint.JOINT_RADIUS, center_y - Joint.JOINT_RADIUS, 
                                   Joint.JOINT_RADIUS*2, Joint.JOINT_RADIUS*2), 0, Joint.ARC_LENGTH)
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))  
            painter.drawEllipse(QRectF(center_x - Joint.JOINT_RADIUS, center_y - Joint.JOINT_RADIUS, 
                                       Joint.JOINT_RADIUS*2, Joint.JOINT_RADIUS*2))   
        if self.next != None:
            self.next.draw(painter)
    
    """ Methods which move the joint when dragged. Rotation method moves all dependent joints recursively. """
    def moveTo(self, x, y): 
        #calculate current mouse cursor angle
        relative_x = x - self.body.x - self.attachment.x
        relative_y = y - self.body.y - self.attachment.y        
        new_angle = math.atan2(-relative_x, relative_y)
        
        angle_rotation = new_angle-self.angle        
        self.rotateBy(angle_rotation)               
    
    def rotateBy(self, by_degree_rad):
        new_angle = self.angle + by_degree_rad
        self.x = self.attachment.x - math.sin(new_angle)*self.length
        self.y = self.attachment.y + math.cos(new_angle)*self.length 
        self.angle = new_angle
        
        if self.next != None:
            self.next.rotateBy(by_degree_rad)
                    
    """ called from the stickman limb class when click is detected """
    def mousePressed(self, event):
        if not event.isProcessed:
            if self.isActive:
                distance = math.sqrt((self.x+self.body.x-event.x)**2+(self.y+self.body.y-event.y)**2)
                if distance <= Joint.JOINT_RADIUS:
                    getWorld().setActive(self.body.name)
                    self.dragged = True
                    event.process()
        
    def mouseReleased(self, event):
        self.dragged = False
        
    def mouseMoved(self, event):
        if self.dragged:
            self.moveTo(event.x, event.y)

class StickMouseEvent():
    
    def __init__(self, x, y):
        self.isProcessed = False
        self.x = x
        self.y = y
    
    def process(self):
        self.isProcessed = True

class World():
    WIDTH = 1100
    HEIGHT = 600
    
    ADD_EVENT = 1
    REMOVE_EVENT = 2
    ACTIVE_EVENT = 3
    
    def __init__(self):
        self.stickmen = list() #active stickman is always at the end of the list
        self.listeners = list()
        self.background = None
        
    """ The draw method first draws the stickmen that are not active, and then the active stickman.
        This technique is required to preserve layering of stickmen. """
    def draw(self, painter):
        if self.background != None:            
            painter.drawImage(QRectF(0, 0, World.WIDTH, World.HEIGHT), self.background, QRectF(0, 0, self.background.width(), self.background.height()))
        for stickman in self.stickmen:
            stickman.draw(painter)
    
    def setBackground(self, background_path):
        self.background = QImage(background_path)
    def clearBackground(self, color):
        self.background = None    
    
    """ Methods necessary to manipulate stickmen in the world"""        
    def getStickman(self, name):
        for stickman in self.stickmen:
            if stickman.name == name:
                return stickman
        return None
    
    def createStickman(self, name, x, y):
        new_stickman = Stickman(name, x, y)
        self.stickmen.append(new_stickman)
        for listener in self.listeners:
            listener(name, World.ADD_EVENT)
       
    def removeStickman(self, name):
        for stickman in self.stickmen:
            if stickman.name == name:
                self.stickmen.remove(stickman)
                for listener in self.listeners:
                    listener(name, World.REMOVE_EVENT)
    
    """ Methods necessary to create frames and set predefined stickmen to the World from the frames """
    def getFrame(self):
        frame = Frame(1)
        frame.stickmen = copy.deepcopy(self.stickmen)
        return frame
    def setWorldFrom(self, frame):        
        self.setStickmen(frame.stickmen)
    def copyWorld(self):
        self.setStickmen(copy.deepcopy(self.stickmen))
    
    #methods used internally
    def setStickmen(self, new_stickmen):
        self.clearAll()
        for new_stickman in new_stickmen:
            self.stickmen.append(new_stickman)
            for listener in self.listeners:
                listener(new_stickman.name, World.ADD_EVENT)
    def clearAll(self):
        for stickman in self.stickmen.copy():
            self.stickmen.remove(stickman)
            for listener in self.listeners:
                listener(stickman.name, World.REMOVE_EVENT)
    
    """ Utility methods """
    def exists(self, name):
        if self.getStickman(name) == None:
            return False
        else:
            return True
    
    def getActive(self):
        if len(self.stickmen) > 0:
            return self.stickmen[len(self.stickmen)-1]
        else:
            return None
    
    """ method called when one of stickmen needs to become active """
    def setActive(self, name):
        search = self.getStickman(name)
        if search != None:
            self.stickmen.remove(search)
            self.stickmen.append(search)
            for listener in self.listeners:
                listener(name, World.ACTIVE_EVENT)
                        
    def isActive(self, name):
        if len(self.stickmen) == 0:
            return False
        elif self.stickmen[len(self.stickmen)-1].name == name:
            return True
        else:
            return False
    
    """ methods for adding listeners to avoid circular imports """
    def addListener(self, listener):
        self.listeners.append(listener)
    
    """called from the canvas, when a click is detected """
    def mousePressed(self, x, y):
        event = StickMouseEvent(x, y)
        for stickman in reversed(self.stickmen):
            if not event.isProcessed:
                stickman.mousePressed(event)
    
    def mouseReleased(self, x, y):
        event = StickMouseEvent(x, y)
        for stickman in reversed(self.stickmen):
            if not event.isProcessed:
                stickman.mouseReleased(event)
            
    def mouseMoved(self, x, y):
        event = StickMouseEvent(x, y)
        for stickman in reversed(self.stickmen):
            if not event.isProcessed:
                stickman.mouseMoved(event)
    
world = World()

""" Function through which the WOrld instance is supposed to be retrieved in other parts of the program """
def getWorld():
    return world



