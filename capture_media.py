import os
import glob
import sys
import re
import time
import subprocess
import MySQLdb as mdb
from picamera import PiCamera
from time import sleep
import datetime
from fractions import Fraction

databaseUsername="root"
databasePassword="password"
databaseName="Temp_DB"

pic_path = "/var/www/pics/"
vid_path = "/var/www/vids/"

def savePicToDB(path):
        con = mdb.connect("localhost",databaseUsername, databasePassword, databaseName)
        currentDateTime = datetime.datetime.now()

        with con:
                cur=con.cursor()
                cur.execute("INSERT INTO pics (path, time) VALUES (%s,%s)", (path,currentDateTime))

                print "Saved pic"
                return "true"

def saveVidToDB(path):
        con = mdb.connect("localhost",databaseUsername, databasePassword, databaseName)
        currentDateTime = datetime.datetime.now()

        with con:
                cur=con.cursor()
                cur.execute("INSERT INTO vids (path, time) VALUES (%s,%s)", (path,currentDateTime))

                print "Saved vid"
                return "true"


def captureMedia():
        camera = PiCamera()
        camera.vflip = False
        camera.hflip = False

        while True:
                if datetime.datetime.now().hour >= 4 && datetime.datetime.now().hour < 22:
                        # only capture media between 4 AM and 10 PM
                        #take pic
                        camera.resolution = (2592, 1944)
                        camera.start_preview()
                        sleep(3)
                        pic_fname = pic_path+str(datetime.datetime.now())+'_image.jpg'
                        camera.capture(pic_fname)
                        camera.stop_preview()
                        savePicToDB(pic_fname)

                        #take vid
                        camera.resolution = (1280, 720)
                        camera.framerate = 25
                        vid_fname = vid_path+str(datetime.datetime.now())+"_vid.h264"
                        camera.start_recording(vid_fname)
                        camera.wait_recording(60)
                        camera.stop_recording()
                        saveVidToDB(vid_fname)
                else: 
                        # sleep for 5 minutes
                        camera = PiCamera(
                                resolution=(1280, 720),
                                framerate=Fraction(1, 6),
                                sensor_mode=3)
                        camera.shutter_speed = 6000000
                        camera.iso = 800
                        sleep(30)
                        camera.exposure_mode = 'off'
                        sleep(300)
captureMedia()
