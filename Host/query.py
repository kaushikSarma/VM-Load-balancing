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

def main():
    VirtualServerQueue = balance.ServerQue()

    app = bottle.app()
    app.install(EnableCors())

    # server route
    @app.route('/',method = 'GET')
    def process():
        return VirtualServerQueue.requestService()

    # functiont to route /stats requests 
    @app.route('/stats',method = 'GET')
    def process():
        toreturn = {}
        #vm_id = int(request.query['id']) + start - 1
        vm_id = int(request.query['id']) - 1
        return VirtualServerQueue.updateStats(vm_id)

    # function to return /numserver requests. Returns the number of active VM
    @app.route('/numservers', method = "GET")
    def getservers():
        return {'n': config.servercount}

    # initiate and run the server
    app.run(host="0.0.0.0", port=8070, debug=True)
    
    pass

if __name__ == '__main__':
    main()