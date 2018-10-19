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

   
from multiprocessing import process
from clint.textui import progress
import requests as req
import os
import json
import numpy as np

class logger:
    errorCode   = "ERROR"
    fetchCode   = "FETCH"
    controlCode = "CONTROL"

    def __init__(self):
        self.config = dict()

    def logMessage(logcode, message):
        print("[{}]".format(logcode) + message)

    def logConfig(key, value):
        self.config[key] = value


class odm(logger):
    def __init__(self, url):
        self.rsrcUrl = url                                      #Populating self with details.
        self.fileName = url.split('/')[-1]                      #Filename
        resp = req.head(self.rsrcUrl)                           #Dummy Fetch
        self.fileSize = int(resp.headers['content-length'])     #Size in bytes

    def writeconfig(self, x):                                   #Passing in tuples of key value pair.
        self.logConfig(str(x[0]), str(x[1]))

    def flushConfig(self):
        cnfData = json.dumps(self.config)
        with open("{}.json".format(self.fileName), 'w') as configFile:
            configFile.write(cnfdata)
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
        #Initial Tantrum
        self.logConfig("FileStatus", "Downloading")
        self.noc = mp.cpu_count()
        self.logConfig("NOC", self.noc)

        #Process calculations
        self.nop = sigmoid(self.fileSize)
        #Defining download pointers.
        distribute()                                            #Distribute the download pointers
    
    def processHandler(self, start, end, instanceNum):
        hdr = {'RANGE':'bytes={},{}'.format(start, end)}
        resp = req.get(self.rsrcUrl, headers=hdr, stream=True)
        with open("{}.part{}".format(self.fileName, instanceNum), 'wb') as file:
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=((end-start)/1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()

    def mergeParts(self):
        with open(self.fileName, 'ab') as file:
            for i in range(1, self.nop+1):
                with open("{}.part{}".format(self.fileName, i), 'rb') as tempFile:
                    file.write(tempFile.read())
                    file.flush()
                    tempFile.close()

    def download(self):
        prcs = []
        for i in range(0, self.nop):
            p = process(target = self.processHandler, args=(self.distrib[i], self.distrib[i+1], i+1,))
            prcs.append(p)
            p.start()
        
        for j in prcs:
            j.join()
