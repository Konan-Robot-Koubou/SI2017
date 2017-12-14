# coding:utf-8

import RPi.GPIO as GPIO
from time import sleep
import subprocess as sp
import sys

#第一引数はRTコンポーネント群の結線情報が含まれるrtsysファイルのパス,第二引数はIPアドレス
args = sys.argv

sleep(10)
switchInputPin = 18 #Input switch value
LEDOutputPin = 17 #Output LED
LEDErr = 10 #Error
rtsysFile = args[1] #rtコンポーネント群の結線情報
adress = args[2]#IPアドレス

class check:
	def ActivateCheck(self):
	#Active状態のコンポーネントの有無を調べる
                return sp.call("rtls -lR /" + adress + " | grep Active | grep -v grep",shell=True)==1
	
	def ErrorCheck(self):
	#Error状態のコンポーネントの有無を調べる
		return sp.call("rtls -lR /" + adress + " | grep Error | grep -v grep",shell=True)==0

class LED:
	def turnOn(self):
		#turn on LED 
		GPIO.output(LEDOutputPin,True)
        
	def turnOff(self):
		#turn off LED
        	GPIO.output(LEDOutputPin,False)
        	
        def turnErrOn(self):
		#Error状態を知らせるLEDを点灯させる
                GPIO.output(LEDErr,True)

        def turnErrOff(self):
		#Error状態を知らせるLEDを消灯させる
                GPIO.output(LEDErr,False)

sp.call("echo y | rtm-naming",shell=True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switchInputPin,GPIO.IN)
GPIO.setup(LEDOutputPin,GPIO.OUT)
GPIO.setup(LEDErr,GPIO.OUT)
LED = LED()
check = check()
LED.turnOff()

sleep(20)

sp.call("rtresurrect " + rtsysFile,shell=True) #結線情報を復元
try:
	while True:

		if check.ErrorCheck() == True:
			sp.call("rtstop " + rtsysFile,shell=True) #コンポーネントをdeactive
			LED.turnErrOn()
			LED.turnOff()

                if GPIO.input(switchInputPin) == 1:
                        if check.ActivateCheck() == True and check.ErrorCheck() == False:
                                LED.turnOn()
                                print "rtstart"
				sp.call("rtstart " + rtsysFile,shell=True) #コンポーネントをActive
		    	elif check.ActivateCheck() == False and check.ErrorCheck() == False:
		        	LED.turnOff()
		        	print "rtstop"
				sp.call("rtstop " + rtsysFile,shell=True) #コンポーネントをdeactive
			elif check.ErrorCheck() == True and check.ActivateCheck() == True:
				#エラー状態のコンポーネントの名前を取得する
				ret = sp.Popen("rtls -lR /" + adress + " | grep Error | grep -v grep",shell=True,stdout=sp.PIPE, stderr=sp.PIPE).communicate()
				compName = ret[0].split(" ")[13].replace("\n","")
				#エラー状態のコンポーネントをリセットする
				sp.call("rtreset /" + adress + "/raspberrypi.host_cxt/" + compName,shell=True)
				LED.turnErrOff()
				LED.turnOn()
				sp.call("rtstart " + rtsysFile,shell=True) #コンポーネントをActive

except KeyboardInterrupt:
    pass

GPIO.cleanup() #GPIO close
    
