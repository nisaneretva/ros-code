#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import numpy as np

class KenarTespit():
    
    def __init__(self):
        
        self.node_name = "kenar_tespit"
        
        rospy.init_node(self.node_name)
        
        self.bridge = CvBridge()
        
        rospy.Subscriber("/usb_cam/image_raw", Image, self.func, queue_size = 1)
        
        rospy.loginfo("Goruntu alindi!")

    def func(self, ros_goruntu):
    
        try:
            cv_goruntu = self.bridge.imgmsg_to_cv2(ros_goruntu, "bgr8")
        
        except CvBridgeError as e:
            print (e)
        
        array_goruntu = np.array(cv_goruntu, dtype=np.uint8)
        
        islenmis_goruntu = self.tespit(array_goruntu)
                       
        cv2.imshow('Kenar Tespiti', islenmis_goruntu)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
           rospy.signal_shutdown('kapatiliyor...')
       
    def tespit(self, array_goruntu):
   
        gri_goruntu = cv2.cvtColor(array_goruntu, cv2.COLOR_BGR2GRAY)
        
        blur_goruntu = cv2.blur(gri_goruntu, (7, 7))
        
        kenarlar = cv2.Canny(blur_goruntu, 15.0, 30.0)
        
        return kenarlar

def main(args):       
    
    try:
        KenarTespit()
        rospy.spin()
    
    except KeyboardInterrupt:
        print ('Kapatiliyor!')
        cv2.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)