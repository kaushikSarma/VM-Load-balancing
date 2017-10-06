prev = -1

def choose(servers):
    ''' Currently implements round robin '''
    global prev
    size = len(servers)
    prev = (prev + 1) % size

    return servers[prev]
