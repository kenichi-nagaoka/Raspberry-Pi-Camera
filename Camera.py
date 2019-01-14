#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sched, time, datetime, threading
import os
from picamera import PiCamera
from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket('test-bucket-0922')
camera = PiCamera()
picPath = '/home/pi/pic/'
stop = None

def processing():
        picName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
        camera.capture(picPath + picName)
        blob = bucket.blob(picName)
        blob.upload_from_filename(picPath + picName)

def schedule():
    s = sched.scheduler(time.time, time.sleep)
    while True:
        print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        s.enter(10, 1, processing, '')
        s.run()
        if stop is not None:
            print('stop thread')
            break
                                                                                                                
def control():
    thread_obj = threading.Thread(target=schedule)
    thread_obj.start()
    while True:
        global stop
        stop = input()
        break
                                                                                                                                                    
if __name__ == '__main__':
    control()
