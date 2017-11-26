from pprint import pprint as pp
import requests
import bottle
from bottle import run, route, request, response
import json
import config 

# server collection datastructure
class ServerQue:
    def __init__(self):
        self.base = config.base
        self.start = config.start
        self.servercount = config.servercount
        self.serverip = generateServerAddress(self.base, self.start, self.servercount)
        self.stats = {}
        self.prev = -1

    def updateStats(self, id):
        if id == -1:
            for index, vm in enumerate(self.serverip):
                try:
                    print("url = " + vm + "/stats")
                    res = requests.get(vm + "/stats")
                    self.stats[index + 1] = json.loads(res.text)
                except:
                    pass
        else:
            self.stats[id + 1]  = json.loads(requests.get(self.stats[id]).text)
        
        return self.stats

    def requestService(self):
        return json.loads(requests.get(self.choose()).text)
    
    def choose(self):
        ''' Currently implements round robin '''
        self.prev = (self.prev + 1) % self.servercount
        print(self.serverip[self.prev])
        return self.serverip[self.prev]


# generate a list of IP addresses for the 
def generateServerAddress(base, start, servercount):
    return [base % str(i) for i in range(start, start + servercount)]

# implementation of round robin
def choose(servers):
    ''' Currently implements round robin '''
    global prev
    size = len(servers)
    prev = (prev + 1) % size
    return servers[prev]