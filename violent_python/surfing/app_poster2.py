import mechanize
import cookielib
import getpass
import BeautifulSoup
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

r = br.open('https://www.cheapoair.com/fpnext/air/remotesearch?&yt=0&from=ATL&to=WAS&fromDt=06/27/2018&toDt=06/29/2018&fromTm=1100&toTm=1100&rt=true&daan=&raan=&dst=&rst=&ad=1&se=0&ch=0&infl=0&infs=0&class=1&airpref=&preftyp=1&searchflxdt=false&IsNS=false&searchflxarpt=false&childAge=&prefT=false')
html = r.read()
print html

#soup = BeautifulSoup(html)
#forms = soup.findAll(name='form')
#for form in forms:
#    print form

#br.form['login_email'] = username
#br.form['login_password'] = \
#        getpass.getpass('Enter password for %s: '%username)
#br.submit()

#print br.response().read()
