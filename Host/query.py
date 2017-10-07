from pprint import pprint as pp
import requests
import bottle
from bottle import run, post, request, response, get, route
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
serverCount = 2

@app.route('/stats',method = 'GET')
def process():
    const = 8080
    response = dict()

    vm_id = int(request.query['id']) + const

    # if id = 0, return status array of all servers 
    if vm_id == const:
        for i in range(1, serverCount+1):
            try:
                print("url = " + "http://localhost:"+str(vm_id + i)+"/stats")
                res = requests.get("http://localhost:"+str(vm_id + i)+"/stats")
                response[str(i)] = json.loads(res.text)
            except:
                pass
    else:
        response[request.query['id']] = json.loads(requests.get("http://localhost:"+str(vm_id)+"/stats").text)
    return response

@app.route('/numservers', method = "GET")
def getservers():
    return {'n': serverCount}

app.install(EnableCors())

app.run(port=8070, debug=True)

