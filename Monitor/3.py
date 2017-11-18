import psutil
from bottle import run, route

# Static variable - stores number of requests processed
count = 0

@route('/stats',method = 'GET')
def process():
    netUtilData = psutil.net_io_counters(pernic=True)
    cpuUtilData = psutil.cpu_percent()
    memUtilData = psutil.virtual_memory()
    count += 1
    return {
        'net': netUtilData,
        'cpu': cpuUtilData,
        'mem': memUtilData,
        'count': count
    }

run(host='localhost', port=8083, debug=True)
