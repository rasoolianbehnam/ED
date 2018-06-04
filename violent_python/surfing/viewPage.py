import urllib2
from anonBrowser import *

use_tor(port=9150)
url = 'http://www.myexternalip.com/raw'
header = {'User-Agent': "Googlebot"}

request = urllib2.Request(url, headers=header)
response = urllib2.urlopen(request)

print response.read()

response.close()
