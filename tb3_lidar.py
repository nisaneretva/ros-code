#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan

def lidar_data (veri):

    """
    adet = len(veri.ranges)
    print ('adet: ', adet)

    print ('1: ', veri.ranges[0])
    print ('90: ' , veri.ranges[89])
    print ('180: ', veri.ranges[179])
    print ('270: ', veri.ranges[269])
    """

    bolgeler = {
        'on1' : min(min(veri.ranges[0:9]), 3.5),
        'on2' : min(min(veri.ranges[349:359]), 3.5),
        'on_sol' : min(min(veri.ranges[10:49]), 3.5),
        'sol' : min(min(veri.ranges[50:89]), 3.5),
        'arka' : min(min(veri.ranges[90:268]), 3.5),
        'sag' : min(min(veri.ranges[269:308]), 3.5),
        'on_sag' : min(min(veri.ranges[309:348]), 3.5),
    }

    print(bolgeler)

if __name__ == '__main__':

    rospy.init_node('tb3_lidar', anonymous=True)

    rospy.Subscriber ('/scan', LaserScan, lidar_data)

    rospy.spin()