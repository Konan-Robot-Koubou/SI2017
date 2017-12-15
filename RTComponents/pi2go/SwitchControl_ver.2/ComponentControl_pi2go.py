# coding:utf-8

import os
from time import sleep
import subprocess as sp
import time, pi2go

pi2go.init()
pi2go.cleanup()


args = sys.argv
rtsysFile = args[1] #rtコンポーネント群の結線情報
adress = args[2]#IPアドレス


sleep(10)

class check:
        def ActivateCheck(self):
        # Active状態のコンポーネントの有無を調べる
                return sp.call("rtls -lR /" + adress + " | grep Active | grep -v grep",shell=True)==1

	def ErrorCheck(self):
	#Error状態のコンポーネントの有無を調べる
		return sp.call("rtls -lR /" + adress + " | grep Error | grep -v grep",shell=True)==0

class LED:
        LEDon = 4095
        LEDoff = 0

        def turnOn(self):
                # turn on LED
                pi2go.setAllLEDs(self.LEDoff, self.LEDon, self.LEDoff)

        def turnOff(self):
                # turn off LED
                pi2go.setAllLEDs(self.LEDon, self.LEDoff, self.LEDoff)

LED = LED()
check = check()
LED.turnOff()
os.system("echo y | rtm-naming") # ネーミングサーバをたてる
sleep(20)
sp.call("rtresurrect " + rtsysFile,shell=True) # 結線情報を復元

try:
        while True:
		if check.ErrorCheck() == True:
			sp.call("rtstop " + rtsysFile,shell=True) #コンポーネントをdeactive
			LED.turnOff()

                if pi2go.getSwitch():
                        if check.ActivateCheck() == True and check.ErrorCheck() == False:
                                LED.turnOn()
                                print "rtstart"
                                sp.call("rtstart " + rtsysFile,shell=True) # コンポーネントをActive
                        elif check.ActivateCheck() == False and check.ErrorCheck() == False:
                                LED.turnOff()
                                print "rtstop"
                                sp.call("rtstop " + rtsysFile,shell=True) # コンポーネントをdeactive
			elif check.ErrorCheck() == True and check.ActivateCheck() == True:
				#エラー状態のコンポーネントの名前を取得する
				ret = sp.Popen("rtls -lR /" + adress + " | grep Error | grep -v grep",shell=True,stdout=sp.PIPE, stderr=sp.PIPE).communicate()
				compName = ret[0].split(" ")[13].replace("\n","")
				#エラー状態のコンポーネントをリセットする
				sp.call("rtreset /" + adress + "/raspberrypi.host_cxt/" + compName,shell=True)
				LED.turnOn()
				sp.call("rtstart " + rtsysFile,shell=True) #コンポーネントをActive

except KeyboardInterrupt:
        pass

finally:
        pi2go.cleanup() # pi2go close
