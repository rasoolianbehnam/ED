import Queue
import threading
import os
import urllib2

threads = 10
target = "http://127.0.0.1"
directory = "./www/html/"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)
web_paths = Queue.Queue()

for r,d,f in os.walk("."):
    for file in f:
        remote_path = "%s/%s" %(r, file)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(file)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s"%(target, path)

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()
            print "[%d] => %s" %(response.code, path)
        except urllib2.HTTPError as error:
            print "Failed %s" % error.code
            pass

for i in range(threads):
    print "Spawinging thread %d" % i
    t = threading.Thread(target=test_remote)
    t.start()
