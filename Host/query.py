from pprint import pprint as pp
import requests
import bottle
from bottle import run, post, request, response, get, route
from balance import choose

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

@app.route('/stats',method = 'GET')
def process():
    const = 8080
    serverCount = 2
    response = []

    vm_id = int(request.query['id']) + const

    # if id = 0, return status array of all servers 
    if vm_id == const:
        for i in range(1, serverCount+1):
            try:
                print("url = " + "http://localhost:"+str(vm_id + i)+"/stats")
                res = requests.get("http://localhost:"+str(vm_id + i)+"/stats")
                response.append(res)
            except:
                pass
    else:
        response = requests.get("http://localhost:"+str(vm_id)+"/stats")

    return response

@app.route('/', method='GET')
def landing():
    #servers = ['http://localhost:8081', 'http://localhost:8082', 'http://google.com']
    servers = ['http://localhost:8081', 'http://localhost:8082']
    chosen = choose(servers)
    return requests.get(chosen)

app.install(EnableCors())

app.run(port=8070, debug=True)

