# coding:utf-8

import RPi.GPIO as GPIO
import os
from time import sleep
import codecs
import subprocess

LCDLocation = '3e'
switchInputPin = 18 #Input switch value
LEDOutputPin = 15 #Output LED

sleep(10)

class ActiveComp:
    def startComp_LineTracer(self):

        #Run Component
        try:
            ret = subprocess.call("sudo python /home/pi/Desktop/RTC/Zumo-comp.py &",shell=True)
        except:
            ret = 1
        self.writeLCD("Zumo",ret)
        try:
            ret = subprocess.call("sudo python /home/pi/Desktop/RTC/LineTracer-comp.py &",shell=True)
        except:
            ret = 1
        self.writeLCD("LineTracer",ret)

        #Wait time
        sleep(0.5)

    def startComp_LCD(self):
        os.system("sudo python /home/pi/Desktop/RTC/ReadingLog.py &")
        os.system("sudo python /home/pi/Desktop/RTC/TwoLinesLCD.py &")
        sleep(0.5)

    def rtshell_LineTracer(self):
        #RTShell Command
	#rtcon is command which connects two component's terminals
	#rtcon /IPadress/PC_Name/ComponetA_Name/ComponentA's Terminal /IPadress/PC_Name/ComponetB_Name/ComponentB's Terminal
        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:VelocityIn /localhost/raspberrypi.host_cxt/LineTracer0.rtc:Velocity")#Connect Component
        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:LineSensors /localhost/raspberrypi.host_cxt/LineTracer0.rtc:LineSensors")#Connect Component

	#rtconf is command which changes Configuration parameter
	#rtconf /IPadress/PC_Name/Component_Name set parameter_value
        os.system("rtconf /localhost/raspberrypi.host_cxt/Zumo0.rtc set Port /dev/ttyACM0")#Change Config
        print "Setting Complete"

        #Wait Time
        sleep(0.5)

    def rtshell_LCD(self):
        #RTShell Command
        os.system("rtcon /localhost/raspberrypi.host_cxt/ReadingLog0.rtc:Output /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc:Input")

	#rtconf is command which changes Configuration parameter
	#rtconf /IPadress/PC_Name/Component_Name set parameter_value
        os.system("rtconf /localhost/raspberrypi.host_cxt/ReadingLog0.rtc set ErrorLog /home/pi/Desktop/RTC/ErrorLog.txt")
        os.system("rtconf /localhost/raspberrypi.host_cxt/ReadingLog0.rtc set SuccessLog /home/pi/Desktop/RTC/SuccessLog.txt")

    def ActiveComp(self):
        #Active component
	#rtact /IPadress/PC_Name/Component_Name
        os.system("rtact /localhost/raspberrypi.host_cxt/ReadingLog0.rtc /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")

    def writeLCD(self,name,state):#make log
        if state == 0:
            f = open('/home/pi/Desktop/RTC/SuccessLog.txt','a')
            ret = subprocess.check_output('date')
            ret = ret.split(" ")
            f.write(ret[2] + " " + ret[1] + " " + ret[3] +"\n")
            f.write(name + "Active\n")
            f.close()
        else:
            f = open('/home/pi/Desktop/RTC/ErrorLog.txt','a')
            ret = subprocess.check_output('date')
            ret = ret.split(" ")
            f.write(ret[2] + " " + ret[1] + " " + ret[3] +"\n")
            f.write(name + "False\n")
            f.close()


class DeactiveComp:
    def Deactive_Comp(self):
        #Deact Component
        print "Stop start"

	#rtdeact /IPadress/PC_Name/Componet_Name
        os.system("rtdeact /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
        os.system("rtdeact /localhost/raspberrypi.host_cxt/ReadingLog0.rtc /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc")

        #Wait time
        sleep(0.5)

    def exit_Comp(self):
        #Component Exit
	#rtexit /IPadress/PC_Name/Component_Name
        os.system("rtexit /localhost/raspberrypi.host_cxt/Zumo0.rtc")
        print "Zumo0.rtc exit"
        os.system("rtexit /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
        print "LineTracer0.rtc exit"
        sleep(3)
        os.system("rtexit /localhost/raspberrypi.host_cxt/ReadingLog0.rtc")
        os.system("rtexit /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc")
        print "All Components exit"

   
class check: 
    def ActivateCheck(self):
        #Check status is Active
	#If component runs in process of Raspberry Pi,ret is 0
        ret = subprocess.call("ps ax | grep Zumo-comp.py | grep -v grep",shell=True)
        return ret == 0

class LED:
    def turnOn(self):
	#turn on LED 
        GPIO.output(LEDOutputPin,True)
        
    def turnOff(self):
	#turn off LED
        GPIO.output(LEDOutputPin,False)

class writeLog:
    def LogMake(self):
        os.system('echo -n  > /home/pi/Desktop/RTC/ErrorLog.txt')
        os.system('echo -n  > /home/pi/Desktop/RTC/SuccessLog.txt')


GPIO.setmode(GPIO.BCM)
GPIO.setup(switchInputPin,GPIO.IN)
GPIO.setup(LEDOutputPin,GPIO.OUT)
LED = LED()
LED.turnOff()
check = check()
writeLog = writeLog()

try:
	while True:
		if GPIO.input(switchInputPin) == 1:
            		if check.ActivateCheck() == True:
                		os.system("echo y | rtm-naming")
                		LED.turnOn()
                		state = ActiveComp()
                		writeLog.LogMake()
                		state.startComp_LCD()
                		state.rtshell_LCD()   
                		state.startComp_LineTracer()
                		state.rtshell_LineTracer()
                		state.ActiveComp()
            		else:
                		LED.turnOff()
                		state = DeactiveComp()
                		state.Deactive_Comp()
                		state.exit_Comp()

                    
except KeyboardInterrupt:
    pass

GPIO.cleanup() #GPIO close
    
