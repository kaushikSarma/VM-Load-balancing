from bottle import run, post, request, response, get, route
from query import landing

clientCount = 15

@route('/requests', method='GET')
def process():
    client_id = request.query['id']
    for i in range(clientCount):
        landing()

run(host='localhost', port=8060, debug=True)
