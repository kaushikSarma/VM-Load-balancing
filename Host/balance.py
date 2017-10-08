import requests
from bottle import run, post, request, response, get, route

prev = -1
serverCount = 4

def generateServerAddress(base, start):
    return [base % str(i) for i in range(start, start + serverCount)]

base = "http://192.168.146.%s:8080/stats"
start = 193
vmList = generateServerAddress(base, start)

def choose(servers):
    ''' Currently implements round robin '''
    global prev
    size = len(servers)
    prev = (prev + 1) % size

    return servers[prev]

@route('/',method = 'GET')
def landing():
    #servers = ['http://localhost:8081', 'http://localhost:8082', 'http://localhost:8083', 'http://localhost:8084']
    chosen = choose(vmList)
    return requests.get(chosen)

run(host='0.0.0.0', port=8071, debug=True)