# Copyright 2018 Utkarsh Bhatt
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
  
import multiprocessing as mp
from clint.textui import progress
import progressbar
import requests as req
import os
import json
import numpy as np

class logger:
    errorCode   = "ERROR"
    fetchCode   = "FETCH"
    controlCode = "CONTROL"

    config = dict()

    def logMessage(self, logcode, message):
        print("[{}]".format(logcode) + message)

    def logConfig(self, key, value):
        self.config[key] = value


class odm(logger):
    def __init__(self, url):
        self.rsrcUrl = url                                      #Populating self with details.
        resp = req.get(self.rsrcUrl, stream=True)               #Dummy Fetch
        self.fileSize = int(resp.headers['content-length'])     #Size in bytes
        if 'filename' in resp.headers['Content-Disposition']:
            self.fileName = str(resp.headers['Content-Disposition']).split('filename=')[1].replace(' ', '_')
        else:
            self.fileName = url.split('/')[-1]                  #Filename

    def writeconfig(self, x):                                   #Passing in tuples of key value pair.
        self.logConfig(str(x[0]), str(x[1]))

    def flushConfig(self):
        cnfData = json.dumps(self.config)
        with open("{}.json".format(self.fileName), 'w') as configFile:
            configFile.write(cnfData)
            configFile.flush()
    
    def sigmoid(self, x): 
        x = x / (1024*1024*512)                                     
        nop =  64 / (1 + 8*(np.exp(-x)))                        #Number of processess.
        if(nop < self.noc):
            return int(nop)
        else:
            return self.noc * int(round(nop / self.noc))

    def distribute(self):
        c = 0
        distrib = list()
        chunkSize = self.fileSize / self.nop
        for i in range(1, self.nop+1):
            distrib.append(c)
            c = i*chunkSize + 1
        distrib.append(self.fileSize)
        self.distrib = distrib

    def compute(self):
        print("Entered compute()")
        #Initial Tantrum
        self.logConfig("FileStatus", "Downloading")
        self.noc = mp.cpu_count()
        self.logConfig("NOC", self.noc)

        #Process calculations
        self.nop = self.sigmoid(self.fileSize)
        #Defining download pointers.
        self.distribute()                                        #Distribute the download pointers

        #setting up tracker and ProgressBar
        self.index = 0
        self.tracker = range(0, self.fileSize)
        self.tracker.append(self.fileSize)
        self.pbar = progressbar.ProgressBar(max_value=self.fileSize, widgets=[progressbar.AdaptiveTransferSpeed(),progressbar.Timer(),progressbar.Bar(),progressbar.ETA()])
    
    def processHandler(self, start, end, instanceNum):
        print("Entered process handler [{}]".format(instanceNum))
        hdr = {'RANGE':'bytes={},{}'.format(start, end)}
        resp = req.get(self.rsrcUrl, headers=hdr, stream=True)
        with open("{}.part{}".format(self.fileName, instanceNum), 'wb') as file:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    self.index = self.index + 1
                    self.pbar.update(self.tracker[self.index])

    def mergeParts(self):
        with open(self.fileName, 'ab') as file:
            for i in range(1, self.nop+1):
                with open("{}.part{}".format(self.fileName, i), 'rb') as tempFile:
                    file.write(tempFile.read())
                    file.flush()
                    tempFile.close()

    def download(self):
        print("Entered download()")
        self.compute()
        prcs = []
        for i in range(0, self.nop):
            p = mp.Process(target = self.processHandler, args=(self.distrib[i], self.distrib[i+1], i+1,))
            prcs.append(p)
            p.start()
        
        for j in prcs:
            j.join()
