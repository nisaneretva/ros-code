#!/usr/bin/enc python
#-*-coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan

def func(veri):

    print (veri)  #verilerin ekrana yazdirilmasi saglanmaktadir

def sonlandir():
    rospy.loginfo('sonlandirildi') #ekrana çıktının sonlandirildigi bilgisi verilmektedir

rospy.init_node('lidar_verileri', anonymous=True) #düğüm tanımlamak için 

rospy.loginfo('Sonlandirmak icin CTRL+C') #kullanıcıya işlem sonlandirması için yapması gerektiği söylenmektedir
rospy.on_shutdown(sonlandir) #on_shutdown fonksiyonu ile işlemin sonlandırılması sağlanmaktadır

rospy.Subscriber('mybot/laser/scan',LaserScan, func) #abone olunan topic yazılımktadır lidare verileri burdan alınmaktadır
rospy.spin() #call back olduğu için spin metodunu kullanıyoruz
