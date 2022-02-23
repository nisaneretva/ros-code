#!/usr/bin/enc python
#-*-coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan

def func(veri):
   # adet=len(veri.ranges)         #lidardan toplam kaç adet veri geldiğini hesaplamak amacıyla kullanılır
   # print('Bir taramada uretilen veri sayı adeti: ', adet)

    bolgeler = {
        'sag' : min(min(veri.ranges[0:143]), 30), #min uzaklık lidara gönderilmelidir 
        'on_sag' : min(min(veri.ranges[144:287]), 30), #30 olmasının sebebi lidar sensörünün mak menzilinin 30 olmasıdır
        'on' : min(min(veri.ranges[288:431]), 30), # inf ile çarpışma olmaması için min,min şeklinde iç içe fonk kullanılmaktadır.
        'on_sol' : min(min(veri.ranges[432:575]), 30),
        'sol' : min(min(veri.ranges[576:719]), 30),
    }
    
    print(bolgeler)


def sonlandir():
    rospy.loginfo('sonlandirildi') #ekrana çıktının sonlandirildigi bilgisi verilmektedir
    

rospy.init_node('lidar_verileri', anonymous=True) #düğüm tanımlamak için 

rospy.loginfo('Sonlandirmak icin CTRL+C') #kullanıcıya işlem sonlandirması için yapması gerektiği söylenmektedir
rospy.on_shutdown(sonlandir) #on_shutdown fonksiyonu ile işlemin sonlandırılması sağlanmaktadır

rospy.Subscriber('mybot/laser/scan',LaserScan, func) #abone olunan topic yazılımktadır lidare verileri burdan alınmaktadır
rospy.spin() #call back olduğu için spin metodunu kullanıyoruz
