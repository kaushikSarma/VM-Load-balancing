import psutil
from bottle import run, route

# Static variable - stores number of requests processed
count = 0

@route('/',method = 'GET')
def process():
    global count
    count += 1
    return {'count': count}


@route('/stats',method = 'GET')
def process():
    global count
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

run(host='0.0.0.0', port=8081, debug=True)
