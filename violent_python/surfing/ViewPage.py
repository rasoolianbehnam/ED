from anonBrowser import *

ab = anonBrowser(proxies=[],\
user_agents=[('User-agent','superSecretBroswer')])
ab.anonymize()
print '[*] Fetching page'
response = ab.open('http://www.gmail.com/')
print response.read()
for cookie in ab.cookie_jar:
    print cookie
