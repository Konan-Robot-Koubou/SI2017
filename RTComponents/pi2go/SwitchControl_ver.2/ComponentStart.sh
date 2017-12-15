#!/bin/sh

sleep 10
##ここから起動するコンポーネントを記述していく
sudo python /home/pi/pi2go/pi2goRTC.py &
sudo python /home/pi/pi2go/IRSensor.py &
