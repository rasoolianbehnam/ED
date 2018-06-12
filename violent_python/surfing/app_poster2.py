import mechanize
import cookielib
import getpass
from BeautifulSoup import BeautifulSoup
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

r = br.open('https://www.imdb.com')
html = r.read()
#print html

for form in br.forms():
    print form

br.select_form(nr=0)
br.form['q'] = 'shawshank redemption'
#br.form['login_password'] = \
#        getpass.getpass('Enter password for %s: '%username)
br.submit()

html = br.response().read()
soup = BeautifulSoup(html)
links = soup.findAll(name='a')
for link in links:
    try:
        href = link['href']
        if '/title/' in href:
            print href
    except:
        pass
