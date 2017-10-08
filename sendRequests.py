from tornado import ioloop
import time
import sys

s = time.time()
maxRequestCount = 1000

i = 0
c = 0
ip = "http://localhost:8071/"

# Suppresses the error from printing
class DevNull:
    i = 0
    c = 0
    def write(self, msg):
        #pass
        # This part of code isn't working, check it out.
        for j in range(1, 20):
            i += 1
            c += 1
            print(c)
            handle_request()

#sys.stderr = DevNull()

def handle_request():
    
    res = requests.get(ip)
    
    global i
    i -= 1

    # Must be used when client count is increased.
    #time.sleep(0.2)

    if i == 0:
        ioloop.IOLoop.instance().stop()

#1000 client requests are processed in 4 seconds.
for j in range(maxRequestCount):
    i += 1
    c += 1
    print(c)
    handle_request()
try:
    ioloop.IOLoop.instance().start()
except ConnectionRefusedError:
    #pass
    print("Interrupt occured, taking break for 2 seconds.")
    time.sleep(2)
    # This loop isn't running, check it out !!
    try:
        for q in range(j, 1000):
            i += 1
            c += 1
            print(c)
            handle_request()
    except ConnectionRefusedError:
        print("Over dude")
        pass

print("Time taken to process = " + str(time.time() - s))