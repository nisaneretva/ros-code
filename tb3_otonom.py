#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def lidar_data (veri):

    bolgeler = {
        'on1' : min(min(veri.ranges[0:9]), 30),
        'on2' : min(min(veri.ranges[349:359]), 30),
        'on_sol' : min(min(veri.ranges[10:49]), 30),
        'sol' : min(min(veri.ranges[50:89]), 30),
        'arka' : min(min(veri.ranges[90:268]), 30),
        'sag' : min(min(veri.ranges[269:308]), 30),
        'on_sag' : min(min(veri.ranges[309:348]), 30),
    }

    print(bolgeler)
    hareket(bolgeler)

def hareket (bolgeler):

    if bolgeler['on1'] and bolgeler['on2'] > 0.8:
        hiz= 0.8

        if bolgeler['on_sag'] - bolgeler['on_sol'] > 1.0:
            print ('Donus: SAG')
            hiz=0.4
            donus = -0.4
        
        elif bolgeler['on_sol'] - bolgeler['on_sag'] > 1.0:
            print ('Donus: SOL')
            hiz=0.4
            donus = 0.4

        else:
            print('Donus: 0')
            hiz=0.8
            donus=0.0
    else:
        print('DUR')
        hiz=0.0
        donus=0.0

    obje.linear.x =hiz
    obje.angular.z=donus
    pub.publish(obje)    

def durdur():
    rospy.loginfo("robot durduruldu")
    pub.publish(Twist())

if __name__ == '__main__':

    rospy.init_node('tb3_otonom',anonymous=True)
    rospy.Subscriber('/scan', LaserScan, lidar_data)
    rospy.loginfo('Sonlandirmak icin CTRL+C')
    rospy.on_shutdown(durdur)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    obje= Twist()
    rospy.spin()