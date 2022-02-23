#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Cizgi:

    def __init__(self):
        
        self.bridge = cv_bridge.CvBridge()
        
        self.image_sub = rospy.Subscriber('camera/image',Image, self.func)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        
        self.twist = Twist()

    def func(self, ros_goruntu):
        
        cv_goruntu = self.bridge.imgmsg_to_cv2(ros_goruntu,'bgr8')
        
        hsv_goruntu = cv2.cvtColor(cv_goruntu, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([ 10, 10, 10])
        upper_yellow = numpy.array([255, 255, 250])
        
        mask = cv2.inRange(hsv_goruntu, lower_yellow, upper_yellow)

        cv2.imshow('maske', mask)
        
        h, w, d = hsv_goruntu.shape
        
        search_top = 3*h/4
        search_bot = 3*h/4 + 20
        
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        
        cv2.imshow('kirpilmis_maske', mask)
        
        M = cv2.moments(mask)
            
        if M['m00'] > 0:
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            cv2.circle(cv_goruntu, (cx, cy), 20, (0,0,255), -1)
            
            err = cx - w/2
        
        self.twist.linear.x = 0.1
        self.twist.angular.z = -float(err) / 100
        self.cmd_vel_pub.publish(self.twist)

        cv2.imshow('cizgi izleme', cv_goruntu)
        cv2.waitKey(3)

if __name__ == "__main__":

    rospy.init_node('cizgi_izleme') 
    obje = Cizgi()
    rospy.spin()