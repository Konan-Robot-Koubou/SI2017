# coding:utf-8

import RPi.GPIO as GPIO
import pi2go
import os
from time import sleep
import subprocess

sleep(10)

class ActiveComp:
    def startComp(self):

        #Run Component
        os.system("sudo python /home/pi/Desktop/RTC/pi2goRTC.py &")
        os.system("sudo python /home/pi/Desktop/RTC/IRSensorRTC.py &")

        #Wait time
        sleep(0.8)

    def rtshell(self):
        #RTShell Command
	#rtcon is command which connects two component's terminals
	#rtcon /IPadress/PC_Name/ComponetA_Name/ComponentA's Terminal /IPadress/PC_Name/ComponetB_Name/ComponentB's Terminal
        os.system("rtcon /localhost/raspberrypi.host_cxt/pi2goRTC0.rtc:SpeedIn /localhost/raspberrypi.host_cxt/IRSensor0.rtc:SpeedOut")#Connect Component
        os.system("rtcon /localhost/raspberrypi.host_cxt/pi2goRTC0.rtc:IRSensor /localhost/raspberrypi.host_cxt/IRSensor0.rtc:IRSensorValue")#Connect Component
        print "Setting Complete"

        #Wait Time
        sleep(0.5)

    def ActiveComp(self):
        #Active component
	#rtact /IPadress/PC_Name/Component_Name
        os.system("rtact /localhost/raspberrypi.host_cxt/IRSensor0.rtc /localhost/raspberrypi.host_cxt/pi2goRTC0.rtc")


class DeactiveComp:
    def Deactive_Comp(self):
        #Deact Component
        print "Deactive start"
	#rtdeact /IPadress/PC_Name/Componet_Name
        os.system("rtdeact /localhost/raspberrypi.host_cxt/pi2goRTC0.rtc /localhost/raspberrypi.host_cxt/IRSensor0.rtc")

        #Wait time
        sleep(0.5)

    def exit_Comp(self):
        #Component Exit
	#rtexit /IPadress/PC_Name/Component_Name
        os.system("rtexit /localhost/raspberrypi.host_cxt/pi2goRTC0.rtc")
        os.system("rtexit /localhost/raspberrypi.host_cxt/IRSensor0.rtc")
        sleep(3)
        print "All Components exit"

   
class check:
    def ActivateCheck(self):
        #Check status is Active
	#If component runs in process of Raspberry Pi,ret is 0
	ret = subprocess.call("ps -ax | grep pi2goRTC.py | grep -v grep",shell=True)
	print ret
	return ret == 1

os.system("echo y | rtm-naming")

check = check()
pi2go.init()

try:
	while True:
		if pi2go.getSwitch() == True:
                   if check.ActivateCheck() == True:
                       state = ActiveComp()   
                       state.startComp()
                       state.rtshell()
                       state.ActiveComp()

                   else:
                       state = DeactiveComp()
                       state.Deactive_Comp()
                       state.exit_Comp()
                    
except KeyboardInterrupt:
    pass
