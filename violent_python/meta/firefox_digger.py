import sqlite3
import sys
import secretstorage
#! /usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Function to get rid of padding
def printCookies(cookieDb, feed_dict, fields, host=None):
    try:
        conn = sqlite3.connect(cookieDb)
        c = conn.cursor()
        command = ''
        for field in fields:
            command += feed_dict[field] + ', '
        command = 'SELECT %s FROM %s'%(command[:-2], feed_dict['table'])
        if host:
            command += ' where %s = \'%s\''%(feed_dict['host'], host)
        command += ';'
        print command
        c.execute(command)
        print '\n[*] --- Found Cookies ---'
        for row in c:
            host = str(row[0])
            name = str(row[1])
            path = str(row[2])
            value = str(row[3])
            print '[+] Host: %s, Cookie: %s, Value: %s, Path: %s' %(host, name, value, path)
            #print '[+] File: ' + str(row[0]) + 'from
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error read your cookies database.'
        else:
            print e

firefox_dict = {'table':'moz_cookies', 'host':'host', 'name':'name', 'path':'path', 'value':'value'}
chrome_dict = {'table':'cookies', 'host':'host_key', 'name':'name', 'path':'path', 'value':'encrypted_value'}
firefox_cookieDB = '/home/bzr0014/.mozilla/firefox/wioz1ykh.default/cookies.sqlite'
chromium_cookieDB = '/home/bzr0014/.config/chromium/Default/Cookies'

fields = ['host', 'value', 'name', 'path']
printCookies(firefox_cookieDB, firefox_dict, fields, 'rapidbaz.ir')

fields = ['host', 'value', 'name', 'path']
printCookies(chromium_cookieDB, chrome_dict, fields, 'rapidbaz.ir')
