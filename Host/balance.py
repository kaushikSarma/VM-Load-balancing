import requests

prev = -1

def choose(servers):
    ''' Currently implements round robin '''
    global prev
    size = len(servers)
    prev = (prev + 1) % size

    return servers[prev]

def landing():
    servers = ['http://localhost:8081', 'http://localhost:8082', 'http://localhost:8083', 'http://localhost:8084']
    chosen = choose(servers)
    return requests.get(chosen)
