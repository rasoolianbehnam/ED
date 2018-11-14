import requests
import sys
import os
import socket
from six.moves import urllib

def download_progress(count, block_size, total_size):
    percent = count * block_size * 100 // total_size
    sys.stdout.write("\rDownloading: %d%%"%percent)
    sys.stdout.flush()

def fetch(url, path='./'):
    file_name = url.split('/')[-1]
    urllib.request.urlretrieve(url, file_name, reporthook=download_progress)
    print('')

url = sys.argv[1]

fetch(url)
