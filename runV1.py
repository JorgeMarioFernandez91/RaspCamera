#!/usr/bin/python
 
import RPi.GPIO as GPIO
import time
import picamera
import datetime
import subprocess
import dropbox
import os

access_token = "token"

#key and secret from the Dropbox developer website
app_key = 'key'
app_secret = 'secret'
 
#file name is the date and time it is recorded
def getFileName():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
 
#function to upload video file ot dropbox
def dropboxUpload(fileToUpload):
    #path in dropbox where save file is located
    dropbox_path='/Apps/SecuritySystemAlpha'
    dbx=dropbox.Dropbox(access_token)
    with open(fileToUpload, 'rb') as f:
        dbx.files_upload(f.read(),dropbox_path+fileToUpload,mute=True) 

    #delete file from pi so not to take up too much space
    os.remove(fileToUpload)
    print("File Remove")

sensorPin = 4
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPin, GPIO.IN)
 
prevState = False
currState = False
 
#camera image is upside down, so this flips the image and also sets the resolution
cam = picamera.PiCamera()
cam.rotation = 180
cam.resolution = (1024, 768)

fileName = ""
 
#Keep looping infinitely waiting to sense motion
while True:
    time.sleep(0.1)
    prevState = currState
    currState = GPIO.input(sensorPin)
    if currState != prevState:
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
            print "Uploading footage to Dropbox..."
            dropboxUpload(fileName)
            print "Complete"