import requests
import re
import sys
import threading
import Queue
import os
import time

MAX_TRIALS = 5
sem = threading.Semaphore()

q = Queue.Queue()
trials = []
shutdown_flag = threading.Event()
shutdown_flag.set()

def main():
    global trials
    curl_text = sys.argv[1]
    replacement_string = sys.argv[2]
    num_last_part = int(sys.argv[3])
    num_threads = int(sys.argv[4])
    num_first_part = 1
    if len(sys.argv) > 5:
        num_first_part = int(sys.argv[5])
    overwrite = False
    if len(sys.argv) > 6:
        if sys.argv[6].lower().find("true") > -1:
            overwrite = True
            print "Overwrite activated"

    c = re.compile("-H '(.*?)'")
    headers = {}
    for line in c.findall(curl_text):
    #    print line
        key = line.split(":")[0]
        value = line[len(key)+2:]
        headers[key] = value

    #print headers

    c = re.compile("curl '(.*?)'")
    url_grand_template = c.search(curl_text).group(1)
    print url_grand_template

    file_name_grand_template = url_grand_template.split("/")[-1]

    c = re.compile("\(.*?\)")
    url_template = c.sub(replacement_string, url_grand_template)
    file_name_template = c.sub(replacement_string, file_name_grand_template)

    for i in range(1, num_last_part+1):
        if not os.path.isfile(file_name_template%i):
            q.put(i)
        else:
            print "file %s already exists"%(file_name_template%i)
            if overwrite:
                print("Overwriting")
                os.remove(file_name_template%i)
                q.put(i)
    trials = [0 for i in range(num_last_part+1)]

    ths = []
    for i in range(num_threads):
        th = threading.Thread(target=download_thread, args=(url_template, file_name_template, headers))
        ths.append(th)
        th.start()
    try:
        for i, th in enumerate(ths):
            th.join()
            print "Thread %d finished"%i
    except KeyboardInterrupt as kex:
        shutdown_flag.clear()
        print("Exitting gracefully...")
        for i, th in enumerate(ths):
            th.join()
            print "Thread %d finished"%i
        print("done!")
        sys.exit(0)

def download_thread(url_template, file_name_template, headers=None):
    global trials
    while shutdown_flag.is_set() and not q.empty():
        i = q.get()
        url, file_name = prepare_url_and_file(url_template, file_name_template, i)
        #sem.acquire()
        #print "%s -> %s"%(url, file_name)
        #sem.release()
        try:
            download(url, file_name, headers)
        except Exception as ex:
            s = str(ex)
            sem.acquire()
            print "Problem: %s : trial %d : %s"%(file_name, trials[i], s)
            sem.release()
            add_back = True
            if s.startswith("400 Client Error"):
                add_back = False
            if add_back and trials[i] < MAX_TRIALS:
                trials[i]+=1
                q.put(i)


def prepare_url_and_file(url_template, file_name_template, i):
    return url_template%i, file_name_template%i


def download(url, file_name, headers=None):
    print(url)
    res = requests.get(url, headers=headers)
    
    res.raise_for_status()
    with open(file_name, 'wb') as f:
        for chunk in res.iter_content(100000):
            f.write(chunk)

if __name__=="__main__":
    main()
