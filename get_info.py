import os
import glob
import sys
import re
import time
import subprocess
import MySQLdb as mdb
import datetime


databaseUsername="root" #YOUR MYSQL USERNAME, USUALLY ROOT
databasePassword="password" #YOUR MYSQL PASSWORD 
databaseName="Temp_DB" #do not change unless you named the Wordpress database with some other name

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def saveToDatabase(temp):

        con=mdb.connect("localhost", databaseUsername, databasePassword, databaseName)
        currentDateTime=datetime.datetime.now()

        with con:
                cur=con.cursor()

                cur.execute("INSERT INTO temperatures (temp_C, temp_F, time) VALUES (%s,%s,%s)",  (temp[0],temp[1],currentDateTime))

                print "Saved temperature"
                return "true"



def read_temp_raw():
        catdata = subprocess.Popen(['cat',device_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

saveToDatabase(read_temp())
