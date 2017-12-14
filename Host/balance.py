import json
import sys
from functools import reduce
from pprint import pprint as pp

import bottle
import requests
from bottle import request, response, route, run
import aiohttp
from gevent import monkey
monkey.patch_all()

import config


# server collection datastructure
class ServerQue:
    def __init__(self):
        self.base = config.base
        self.start = config.start
        self.servercount = config.servercount
        self.serverip = generateServerAddress(self.base, self.start, self.servercount)
        self.stats = {}
        self.currentAllocationCounts = [ 0 ] * self.servercount
        self.prev = -1
        self.tempVmId = -1

    def updateStats(self, id):
        if id == -1:
            for index, vm in enumerate(self.serverip):
                try:
                    # print("url = " + vm + "/stats")
                    res = requests.get(vm + "/stats")
                    self.stats[index + 1] = json.loads(res.text)
                except:
                    pass
        else:
            self.stats[id + 1]  = json.loads(requests.get(self.serverip[id]).text)
        
        return self.stats

    async def requestService(self):
        chosen = self.enhancedActiveVMLoadBalancer()
        # chosen = self.activeVMLoadBalancer()
        self.currentAllocationCounts[chosen] += 1
        async with aiohttp.ClientSession() as session:
            async with session.get(self.serverip[chosen]) as resp:
                # print(resp.status)
                return await resp.text()
        
    def activeVMLoadBalancer(self):
        '''
            vmStateList:                Dict<vmId, vmState>
            currentAllocationCounts:    Dict<vmId, currentActiveAllocationCount>
        '''
        vmStateList = self.stats
        currentAllocationCounts = self.currentAllocationCounts

        tempVmId = self.tempVmId
        vmId = -1

        totalAllocations = reduce(lambda x, y: x + y, currentAllocationCounts)
        # print(totalAllocations, vmStateList)
        if(totalAllocations < len(vmStateList)):
            for i, vm in enumerate(vmStateList):
                if(currentAllocationCounts[i] == 0):
                    vmId = i
                    break
        else:
            minCount = sys.maxsize
            for i, vm in enumerate(vmStateList):
                curCount = currentAllocationCounts[i]

                if(curCount < minCount):
                    vmId = i

        tempVmId = vmId
        # print("Returning, ", vmId - 1)
        return vmId - 1
    
    def enhancedActiveVMLoadBalancer(self):
        '''
            vmStateList:                Dict<vmId, vmState>
            currentAllocationCounts:    Dict<vmId, currentActiveAllocationCount>
        '''
        vmStateList = self.stats
        currentAllocationCounts = self.currentAllocationCounts

        tempVmId = self.tempVmId
        vmId = -1

        totalAllocations = reduce(lambda x, y: x + y, currentAllocationCounts)
        # print(totalAllocations, vmStateList)
        if(totalAllocations < len(vmStateList)):
            for i, vm in enumerate(vmStateList):
                if(currentAllocationCounts[i] == 0):
                    vmId = i
                    break
        else:
            minAvg = sys.maxsize
            # pp(vmStateList)
            for i in vmStateList:
                curAvg = average(self.stats[i]) 
                if(curAvg < minAvg):
                    minAvg = curAvg
                    vmId = i
                    
        tempVmId = vmId
        # print("Returning, ", vmId - 1)
        return vmId - 1

    def choose(self):
        ''' Currently implements round robin '''
        self.prev = (self.prev + 1) % self.servercount
        print(self.serverip[self.prev])
        return self.serverip[self.prev]


# generate a list of IP addresses for the
def generateServerAddress(base, start, servercount):
    return [base % str(i) for i in range(start, start + servercount)]

def average(stats):
    return (stats['cpu'] + stats['mem'])/200


VirtualServerQueue = ServerQue()

# temp = ServerQue()
# temp.updateStats(-1)
# ch = temp.enhancedActiveVMLoadBalancer()
# print(ch)
