from pprint import pprint as pp
import requests
import bottle
from bottle import run, route, request, response
import json

# import balancer functions
import balance
# import global config variables
import config

# class to deal with CORS errors 
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

# list of VM ip addresses
vmList = balance.generateServerAddress(config.base, config.start, config.serverCount)

# functiont to route /stats requests 
@app.route('/stats',method = 'GET')
def process():
    toreturn = {}

    #vm_id = int(request.query['id']) + start - 1
    vm_id = int(request.query['id']) - 1
    # if id = 0, return status array of all servers 
    if vm_id == -1:
        for index, vm in enumerate(vmList):
            try:
                print("url = " + vm)
                res = requests.get(vm)
                toreturn[index + 1] = json.loads(res.text)
            except:
                pass
    else:
        toreturn[vm_id + 1]  = json.loads(requests.get(vmList[vm_id]).text)
    
    return toreturn

# function to return /numserver requests. Returns the number of active VM
@app.route('/numservers', method = "GET")
def getservers():
    return {'n': config.serverCount}

app.install(EnableCors())

# initiate and run the server
app.run(host="0.0.0.0", port=8070, debug=True)

