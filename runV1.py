#!/usr/bin/python
 
import RPi.GPIO as GPIO
import time
import picamera
import datetime
import subprocess
import dropbox
import os

#access token: MHQU8ikz2LAAAAAAAAAAfW3NoCKAuBFUnPNAdRzrMEtuPYlVQc-9gEXi6xCyIRs7

# Get your app key and secret from the Dropbox developer website
app_key = '3ef0ygak70uki01'
app_secret = 'lqpa4iqas30m1ec'
 
def getFileName():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
 

 
def dropboxUpload(fileToUpload):

    dropbox_path='/Apps/SecuritySystemAlpha'
    dbx=dropbox.Dropbox("MHQU8ikz2LAAAAAAAAAAfW3NoCKAuBFUnPNAdRzrMEtuPYlVQc-9gEXi6xCyIRs7")
    with open(fileToUpload, 'rb') as f:
        dbx.files_upload(f.read(),dropbox_path+fileToUpload,mute=True) # The change from f to f.read() was made to comply with the late-2016 change in the API.

    #delete file from pi so not to take up too much space
    os.remove(fileToUpload)
    print("File Remove")

sensorPin = 4
 
GPIO.setmode(GPIO.BCM)
#GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sensorPin, GPIO.IN)
 
prevState = False
currState = False
 
cam = picamera.PiCamera()
cam.rotation = 180
cam.resolution = (1024, 768)

fileName = ""
 
while True:
    time.sleep(0.1)
    prevState = currState
    currState = GPIO.input(sensorPin)
    if currState != prevState:
        #newState = "HIGH" if currState else "LOW"
        #print "GPIO pin %s is %s" % (sensorPin, newState)
        if currState:
            fileName = getFileName()
            print "Starting Recording..."
            cam.start_preview()
            cam.start_recording(fileName)
            print (fileName)
        else:
            cam.stop_preview()
            cam.stop_recording()
            print "Stopped Recording"
            #print "Sending Mail Notification..."
            #subprocess.call("mail -s 'Motion Detected' jmferna91@gmail.com < /home/pi/message.txt", shell=True)
            #print "Complete"
            print "Uploading footage to Dropbox..."
	    #testing
	    #fileName = "./message1.txt"
            dropboxUpload(fileName)
            print "Complete"