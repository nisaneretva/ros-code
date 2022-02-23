#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

class YuzTespit():
   
    def __init__(self):
 
        self.node_name = "yuz_tespit"
        
        rospy.init_node(self.node_name)
        
        self.bridge = CvBridge()
        
        rospy.Subscriber("/usb_cam/image_raw", Image, self.func, queue_size = 1)
        
        rospy.loginfo("Goruntu alindi!")

    def func(self, ros_goruntu):
    
        try:
            cv_goruntu = self.bridge.imgmsg_to_cv2(ros_goruntu, "bgr8")
        
        except CvBridgeError as e:
            print (e)
   
        islenmis_goruntu = self.tespit(cv_goruntu)
                       
        cv2.imshow('Yuz Tespiti', islenmis_goruntu)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
           rospy.signal_shutdown('kapatiliyor...')
       
    def tespit(self, cv_goruntu):
   
        gri_goruntu = cv2.cvtColor(cv_goruntu, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
        
        yuzler = face_cascade.detectMultiScale(
            gri_goruntu,
            scaleFactor=1.1, #görüntüyü küçültme ölçeği
            minNeighbors=5, #komşu dikdörtgen sayısı
            minSize=(30, 30) #minumum nesne boyutu
    )

        for (x, y, w, h) in yuzler:
            cv2.rectangle(cv_goruntu, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # (cv_goruntu,dikdortgenin sol-ust kose kord.,sag-alt kose koordinatları,
            # dikdortgen rengi,dikdortgen kalinligi)

        return cv_goruntu

def main(args):       
    
    try:
        YuzTespit()
        rospy.spin()
    
    except KeyboardInterrupt:
        print ('Kapatiliyor!')
        cv2.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
