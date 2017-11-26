import sys
from functools import reduce

tempVmId = -1

def enhancedActiveVMLoadBalancer(vmStateList, currentAllocationCounts):
    '''
        vmStateList:                Dict<vmId, vmState>
        currentAllocationCounts:    Dict<vmId, currentActiveAllocationCount>
    '''

    global tempVmId
    vmId = -1

    totalAllocations = reduce(lambda x, y: x + y, currentAllocationCounts)

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
                if(i != tempVmId):
                    vmId = i
                    break

    tempVmId = vmId
    print("Returning, ", vmId)
    return vmId


enhancedActiveVMLoadBalancer([
    {'cpu': 10, 'mem': 10},
    {'cpu': 17, 'mem': 40},
    {'cpu': 40, 'mem': 20},
    {'cpu': 80, 'mem': 15}
], [1, 4, 1, 1])
