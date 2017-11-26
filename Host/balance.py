# generate a list of IP addresses for the 
def generateServerAddress(base, start, serverCount):
    return [base % str(i) for i in range(start, start + serverCount)]

# implementation of round robin
def choose(servers):
    ''' Currently implements round robin '''
    global prev
    size = len(servers)
    prev = (prev + 1) % size
    return servers[prev]