import os
import re
import sys
import ctypes
import getopt
import io
import urllib
import cv2
import time

from datetime import datetime
from urllib.request import Request 
from urllib.request import urlopen
from bs4 import BeautifulSoup
from imageai.Detection import ObjectDetection
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dates

system_info = '(X11; Linux x86_64)'
platform = 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
html_user_agent = 'Mozilla/5.0 '+ system_info +' ' + platform
html_headers = {'User-Agent': html_user_agent}
html_features = "html.parser"

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()

sleep_time = 0

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]
unixOptions = "o:f:t:"

arguments, _ = getopt.getopt(argumentList, unixOptions)

for currentArgument, currentValue in arguments:
    if currentArgument == "-t":
        sleep_time = currentValue


class Crawler:
    def __init__(self):
        self.cameraDetails = {'id': False, 'insecamURL': False, 'directURL': False}
        self.downloadFolder = "images"
        self.oneCamera = False
        self.timeStamp = True

        for currentArgument, currentValue in arguments:
            if currentArgument == "-o":
                self.cameraDetails['id'] = currentValue
                self.oneCamera = True
            elif currentArgument == "-f":
                self.downloadFolder = "images/{}".format(currentValue)
                self.recogFolder = "recog_images/{}".format(currentValue)
        self.main()

    def CreateDir(self, dirName):
        try:
            os.makedirs(dirName)
            print("Created directory {}".format(dirName))
        except FileExistsError:
            pass

    def GetDetails(self):
        self.cameraDetails['insecamURL'] = 'https://www.insecam.org/en/view/{}/'.format(self.cameraDetails['id'])

        req = Request(url=self.cameraDetails['insecamURL'], headers=html_headers)

        soup = BeautifulSoup(urlopen(req).read(), features=html_features)

        for img in soup.findAll('img'):
            if img.get('id') == "image0":
                if img.get('src') == "/static/no.jpg":
                    self.cameraDetails['directURL'] = "NOT FOUND"
                else:
                    self.cameraDetails['directURL'] = "http://{}".format(urllib.parse.urlparse(img.get('src')).netloc)

    def WriteImage(self, cameraID, cameraURL, downloadFolder, recogFolder, totalCams):
        vidObj = cv2.VideoCapture(cameraURL)
        success, image = vidObj.read()
        if success:
            if self.timeStamp:
                timestampStr = datetime.now().strftime("-[%Y-%m-%d]-[%H-%M-%S]")
            cv2.imwrite('{}/{}{}.jpg'.format(downloadFolder,cameraID, timestampStr), image)
            print('Image saved to {}/{}{}.jpg'.format(downloadFolder, cameraID, timestampStr))
            print('Scraped image from camera ID {}'.format(cameraID))

            inpath = execution_path + "/" + downloadFolder + "/" + cameraID + timestampStr + ".jpg"
            outpath = execution_path + "/" + recogFolder + "/" + cameraID + timestampStr + ".jpg"
            detections = detector.detectObjectsFromImage(input_image=inpath, output_image_path=outpath)
            print('Object recognition done on {}/{}{}.jpg'.format(downloadFolder, cameraID, timestampStr))

            counts = {}
            for j in detections:
                if j["name"] not in counts.keys():
                    counts[j["name"]] = 0
                counts[j["name"]] += 1
                
            line = timestampStr + "\n"
            for key in counts.keys():
                line += key + " " + str(counts[key]) + "\n"
            line += "-------------------------\n"
            
            filepath = execution_path + "/" + cameraID + ".txt"
            with open(filepath, 'a') as f:
                f.write(line)
        if not success:
            print("Failed to scrape camera ID {}".format(cameraID))

    def ScrapeOne(self, cameraID):
        self.cameraDetails['insecamURL'] = 'https://www.insecam.org/en/view/{}/'.format(cameraID)
        self.CreateDir(self.downloadFolder)
        self.CreateDir(self.recogFolder)
        req = Request(url=self.cameraDetails['insecamURL'], headers=html_headers)

        cameraName = cameraID
        soup = BeautifulSoup(urlopen(req).read(), features=html_features)
        for img in soup.findAll('img'):
            if img.get('id') == "image0":
                self.WriteImage(cameraName, img.get('src'),self.downloadFolder, self.recogFolder, 1)

    def main(self):
        self.GetDetails()
        self.ScrapeOne(self.cameraDetails['id'])


while(True):
    start = time.time()
    print("Sleep time: {}".format(sleep_time))
    Crawler()
    end = time.time()
    elap_time = end - start
    if float(sleep_time) > elap_time:
        time.sleep(float(sleep_time)-elap_time)
