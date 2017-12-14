#!/bin/sh

sleep 15
##ここから起動するコンポーネント群を書いていく
sudo python /home/pi/Desktop/RTC/Zumo.py &
sudo python /home/pi/Desktop/RTC/LineTracer.py &
