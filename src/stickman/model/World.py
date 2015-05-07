'''
Created on Apr 26, 2015

@author: Artem
'''

from PyQt5.Qt import QPen, QRectF, QPoint
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QLine
import math

class Stickman():
    
    ARM_LENGTH = 80
    HAND_LENGTH = 90
    LEG_LENGTH = 95
    TOE_LENGTH = 30
    
    def __init__(self, name, x, y):
        self.name = name        
        self.x = x
        self.y = y
        self.initBody()
        
    def moveTo(self, x, y):
        self.x = x
        self.y = y
    
    def initBody(self):
        self.head = Head(self)
        self.spine = Spine(self)
        self.joints = list()
        
        """ CREATING LEFT ARM """
        left_arm_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.NECK_LENGTH)
        
        left_elbow_coordinate = left_arm_attachment.getDependentJointCoordinate(Stickman.ARM_LENGTH, 55)
        left_elbow = Joint(self, True, left_elbow_coordinate.x(), left_elbow_coordinate.y())
        left_arm_attachment.setDependentAttachment(left_elbow)
        
        left_hand_coordinate = left_elbow.getDependentJointCoordinate(Stickman.HAND_LENGTH, 135)
        left_hand = Joint(self, True, left_hand_coordinate.x(), left_hand_coordinate.y())
        left_elbow.setDependentAttachment(left_hand)
        
        self.joints.append(left_arm_attachment)
        self.joints.append(left_elbow)
        self.joints.append(left_hand)
        
        """ CREATING RIGHT ARM """
        right_arm_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.NECK_LENGTH)
        
        right_elbow_coordinate = left_arm_attachment.getDependentJointCoordinate(Stickman.ARM_LENGTH, -45)
        right_elbow = Joint(self, True, right_elbow_coordinate.x(), right_elbow_coordinate.y())
        right_arm_attachment.setDependentAttachment(right_elbow)
                
        right_hand_coordinate = right_elbow.getDependentJointCoordinate(Stickman.HAND_LENGTH, -35)
        right_hand = Joint(self, True, right_hand_coordinate.x(), right_hand_coordinate.y())
        right_elbow.setDependentAttachment(right_hand)
        
        self.joints.append(right_arm_attachment)
        self.joints.append(right_elbow)
        self.joints.append(right_hand)
        
        """ CREATING LEFT LEG """
        left_leg_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.SPINE_LENGTH)
        
        left_knee_coordinate = left_leg_attachment.getDependentJointCoordinate(Stickman.LEG_LENGTH, 25)
        left_knee = Joint(self, True, left_knee_coordinate.x(), left_knee_coordinate.y())
        left_leg_attachment.setDependentAttachment(left_knee)
        
        left_foot_coordinate = left_knee.getDependentJointCoordinate(Stickman.LEG_LENGTH, 0)
        left_foot = Joint(self, True, left_foot_coordinate.x(), left_foot_coordinate.y())
        left_knee.setDependentAttachment(left_foot)
        
        left_toe_coordinate = left_foot.getDependentJointCoordinate(Stickman.TOE_LENGTH, 90)
        left_toe = Joint(self, False, left_toe_coordinate.x(), left_toe_coordinate.y())
        left_foot.setDependentAttachment(left_toe)
        
        self.joints.append(left_leg_attachment)
        self.joints.append(left_knee)
        self.joints.append(left_foot)
        self.joints.append(left_toe)
        
        """ CREATING RIGHT LEG """
        right_leg_attachment = Joint(self, False, 0, Head.HEAD_RADIUS + Spine.SPINE_LENGTH)
        
        right_knee_coordinate = right_leg_attachment.getDependentJointCoordinate(Stickman.LEG_LENGTH, -25)
        right_knee = Joint(self, True, right_knee_coordinate.x(), right_knee_coordinate.y())
        right_leg_attachment.setDependentAttachment(right_knee)
        
        right_foot_coordinate = right_knee.getDependentJointCoordinate(Stickman.LEG_LENGTH, 0)
        right_foot = Joint(self, True, right_foot_coordinate.x(), right_foot_coordinate.y())
        right_knee.setDependentAttachment(right_foot)
        
        right_toe_coordinate = right_foot.getDependentJointCoordinate(Stickman.TOE_LENGTH, -90)
        right_toe = Joint(self, False, right_toe_coordinate.x(), right_toe_coordinate.y())
        right_foot.setDependentAttachment(right_toe)
        
        self.joints.append(right_leg_attachment)
        self.joints.append(right_knee)
        self.joints.append(right_foot)
        self.joints.append(right_toe)
                        
    def setHappy(self):
        self.head.expression.setExpression(Expression.SMILE)
    def setSad(self):
        self.head.expression.setExpression(Expression.SAD)
    def setConfused(self):
        self.head.expression.setExpression(Expression.CONFUSED)
        
    def draw(self, painter):
        self.head.draw(painter)
        self.spine.draw(painter)
        
        #first draw black limbs so that they are hidden under white joints
        for joint in self.joints:
            if joint.attachment != None:            
                painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))        
                painter.drawLine(QLine(self.x + joint.attachment.getRelativeCenterPoint().x(), self.y + joint.attachment.getRelativeCenterPoint().y(),
                                       self.x + joint.getRelativeCenterPoint().x(), self.y + joint.getRelativeCenterPoint().y()))
        # next draw joints themselves, so that they are drawn over black limbs
        for joint in self.joints:
            joint.draw(painter)
    
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
    
    def __init__(self, body):
        self.body = body
        self.expression = Expression(body)
        self.dragged = False
    
    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        
        painter.drawArc(QRectF(self.body.x-Head.HEAD_RADIUS, self.body.y-Head.HEAD_RADIUS, Head.HEAD_RADIUS*2, Head.HEAD_RADIUS*2), 0, 16*360) 
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
    
    def __init__(self, body):
        self.body = body
        self.expression = Expression.SMILE
    
    def draw(self, painter):        
        painter.setBrush(QBrush(Qt.SolidPattern))
        
        painter.drawEllipse(QRectF(self.body.x-30, self.body.y-25, Expression.EYE_WIDTH, Expression.EYE_WIDTH))
        painter.drawEllipse(QRectF(self.body.x+15, self.body.y-25, Expression.EYE_WIDTH, Expression.EYE_WIDTH))        
        
        if self.expression == Expression.SMILE:
            self.drawSmile(painter)
        elif self.expression == Expression.SAD:
            self.drawSad(painter)
        else:
            self.drawConfused(painter)        
    
    def setExpression(self, expression):
        self.expression = expression
    
    def drawSmile(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/2, self.body.y-Expression.SMILE_WIDTH/2, Expression.SMILE_WIDTH, Expression.SMILE_WIDTH), 9*360, 6*360)
    def drawSad(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/2, self.body.y+Expression.SMILE_WIDTH/7, Expression.SMILE_WIDTH, Expression.SMILE_WIDTH), 1.5*360, 5*360)
    def drawConfused(self, painter):
        painter.drawArc(QRectF(self.body.x-Expression.SMILE_WIDTH/3.4, self.body.y, Expression.SMILE_WIDTH/1.7, Expression.SMILE_WIDTH/2), 0, 16*360)

class Spine():
    
    NECK_LENGTH = 40
    SPINE_LENGTH = 180
    
    def __init__(self, body):
        self.body = body
    
    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))        
        painter.drawLine(QLine(self.body.x, self.body.y+Head.HEAD_RADIUS, self.body.x, self.body.y+Head.HEAD_RADIUS+Spine.SPINE_LENGTH))

class Joint():
    
    JOINT_RADIUS = 10
    
    """ initialize the joint. The position of the joint is relative to the stickman`s head center """
    def __init__(self, body, isActive, relative_x, relative_y):        
        self.body = body
        self.isActive = isActive
        self.x = relative_x
        self.y = relative_y
        self.attachment = None  #attachment is another joint which is dependent on this one
        self.dragged = False
    
    """ calculate the relative coordinates of the new joints using the given length and degrees of rotation from the current joint """
    def getDependentJointCoordinate(self, length, degree):
        degree_rad = math.radians(degree)
        relative_x = math.sin(degree_rad)*length
        relative_y = math.cos(degree_rad)*length
        return QPoint(self.getRelativeCenterPoint().x()-relative_x, self.getRelativeCenterPoint().y()+relative_y)
    
    def setDependentAttachment(self, attachment):
        self.attachment = attachment
    
    def setActive(self, isActive):
        self.isActive = isActive    
    
    """ methods for the retrieval of the center point of the joint """
    def getRelativeCenterPoint(self):
        return QPoint(self.x, self.y)
    def setRelativeCenterPoint(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, painter):        
        if self.isActive:
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawArc(QRectF(self.body.x + self.getRelativeCenterPoint().x() - Joint.JOINT_RADIUS, self.body.y + self.getRelativeCenterPoint().y() - Joint.JOINT_RADIUS, 
                                   Joint.JOINT_RADIUS*2, Joint.JOINT_RADIUS*2), 0, 16*360)
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))  
            painter.drawEllipse(QRectF(self.body.x + self.getRelativeCenterPoint().x() - Joint.JOINT_RADIUS, self.body.y + self.getRelativeCenterPoint().y() - Joint.JOINT_RADIUS, 
                                       Joint.JOINT_RADIUS*2, Joint.JOINT_RADIUS*2))            
    
    """ Method which moves the joint when dragged """
    def moveTo(self, x, y):
        relative_x = x - self.body.x
        relative_y = y - self.body.y
        self.x = relative_x
        self.y = relative_y
    
    """ called from the stickman limb class when click is detected """
    def mousePressed(self, event):
        if not event.isProcessed:
            if self.isActive:
                distance = math.sqrt((self.x+self.body.x-event.x)**2+(self.y+self.body.y-event.y)**2)
                if distance <= Joint.JOINT_RADIUS:
                    getWorld().setActive(self.body.name)
                    self.dragged = True
                    self.body.joints.remove(self)
                    self.body.joints.append(self)
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
        
    """ The draw method first draws the stickmen that arenot active, and then the active stickman.
        This technique is required to preserve layering of stickmen. """
    def draw(self, painter):
        for stickman in self.stickmen:
            stickman.draw(painter)
                    
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
                    
    def exists(self, name):
        if self.getStickman(name) == None:
            return False
        else:
            return True
    
    def getActive(self):
        return self.stickmen[len(self.stickmen)-1]
    
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
    def addStickmanListener(self, stickmanListener):
        self.listeners.append(stickmanListener)
    
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

def getWorld():
    return world



