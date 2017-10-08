from pprint import pprint as pp
import requests
import bottle
from bottle import run, route
from balance import choose
import json

class EnableCors(object):
    name = 'enable_cors'

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()
serverCount = 4

def generateServerAddress(base, start):
    return [base % str(i) for i in range(start, start + serverCount)]

base = "http://192.168.146.%s:8080/stats"
start = 193
vmList = generateServerAddress(base, start)

@app.route('/stats',method = 'GET')
def process():
    response = {}

    #vm_id = int(request.query['id']) + start - 1
    vm_id = int(request.query['id']) - 1
    # if id = 0, return status array of all servers 
    if vm_id == -1:
        for index, vm in enumerate(vmList):
            try:
                print("url = " + vm)
                res = requests.get(vm)
                response[index + 1] = json.loads(res.text)
            except:
                pass
    else:
        response[vm_id + 1]  = json.loads(requests.get(vmList[vm_id]).text)
    
    return response

@app.route('/numservers', method = "GET")
def getservers():
    return {'n': serverCount}

@app.route('/consumeMemory', method='GET')
def consume():
    arr_size = request.query['id'] - 1

    for index, vm in enumerate(vmList):
        try:
            print("url = " + vm)
            res = requests.get(vm)
            response[index + 1] = json.loads(res.text)
        except:
            pass

app.install(EnableCors())

app.run(host='0.0.0.0', port=8070, debug=True)

