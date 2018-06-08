import sqlite3

def printCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        command = 'select host, name, value from moz_cookies'
        c.execute(command)
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print '[+] Host: %s, Cookie: %s, value: %s' % (host, name, value)
    except Exception, e:
        print e


firefix_dir = '/home/bzr0014/.mozilla/firefox/nmveq1jm.default/'
cookiesDB = firefix_dir + 'cookies.sqlite'
printCookies(cookiesDB)
