import psutil
from bottle import run, post, request, response, get, route

@route('/stats',method = 'GET')
def process():
    netUtilData = psutil.net_io_counters(pernic=True)
    cpuUtilData = psutil.cpu_percent()
    memUtilData = psutil.virtual_memory()
    return {
        'net': netUtilData,
        'cpu': cpuUtilData,
        'mem': memUtilData
    }

run(host='localhost', port=8084, debug=True)
