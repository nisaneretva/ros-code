#!/usr/bin/enc python
#-*-coding: utf-8 -*-
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist #robotun hareketini sağlayacak mesajları yayınlamak için Twist kullanılmaktadır 

def lidar_data(veri):
    bolgeler = {
        'sag' : min(min(veri.ranges[0:143]), 10), #min uzaklık lidara gönderilmelidir 
        'on_sag' : min(min(veri.ranges[144:287]), 10), #30 olmasının sebebi lidar sensörünün mak menzilinin 30 olmasıdır
        'on' : min(min(veri.ranges[288:431]), 10), # inf ile çarpışma olmaması için min,min şeklinde iç içe fonk kullanılmaktadır.
        'on_sol' : min(min(veri.ranges[432:575]), 10),
        'sol' : min(min(veri.ranges[576:719]), 10),
    }
    print (bolgeler)
    hareket (bolgeler)

def hareket (bolgeler): #robot sag duvarı referans alarak kendini ortalamaya çalışacaktır

    if bolgeler['on'] > 0.7: #robotun gideceği alan kalmadığında durması için if else tanımlıyoruz burda gidecek yer kalmadığında 36 satır devreye girecektir
        hiz = 0.4

        if bolgeler['sag'] < 1.1 or bolgeler['on_sag'] < 1.1:
            print('Donus:SOL')
            hiz=0.4
            donus=0.6

        elif bolgeler['sag'] > 2.1 or bolgeler['on_sag'] > 2.1:
            print('Donus:SAG')
            hiz=0.4
            donus=-0.6 #eksi kullanılmasın robotun hareketinin saga doğru + kullanılması sola doğru olmasını sağlar
        else:
            print('Donus:0')
            hiz=0.4
            donus=0.0
    else:
        print('DUR')
        hiz=0.0
        donus=0.0
    
    obje.linear.x = hiz #robotun hız değerine ulaşmak
    obje.angular.z = donus #robotun dönüş değerine ulaşmak 
    pub.publish(obje) #robotu hareket ettiricek mesajları yayınlamak için

def durdur():
    rospy.loginfo("Robot durduruldu")
    pub.publish(Twist()) #robotun hareketi sonlanması için boş degerler gönderiliyor

if __name__ == '__main__':

    rospy.init_node('otonom_bir', anonymous=True) #dugumun tanımlanması
    rospy.Subscriber('/mybot/laser/scan', LaserScan, lidar_data)  #lidar verilerinin alındığı topic tanımlanıyor ayrıca lidar verisi anlamlandırılarak hareketi sağlanıyor robotun

    rospy.loginfo("Sonlandirmak için CTRL+C") #robot du rdugunda veri aktarımı duruyor fakar hareketi devam ediyor bu yüzden 46 satır kullanıyoruz
    rospy.on_shutdown(durdur)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1) #topic tanımlanarak twist tanımlanmaktadır
    obje = Twist() #twist sınıfından bir obje oluşturularak robotun hareketi sağlanmaktadır
    rospy.spin()



