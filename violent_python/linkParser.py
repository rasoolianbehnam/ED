import optparse
from anonBrowser import *
import os
import re
from BeautifulSoup import BeautifulSoup

def printLinks(url, indent=0, ab=None):
    if ab is None:
        ab = anonBrowser()
        ab.anonymize()
    indentation = ""
    for i in range(indent):
        indentation += "    "
    try:
        page = ab.open(url)
        html = page.read()
    except:
        if not indent:
            print '[!!!] Exception. Cannot open page'
        return
#    try:
#        print '[+] Printing Links From Regex.'
#        link_finder = re.compile('href="(.*?)"')
#        links = link_finder.findall(html)
#        for link in links:
#            print link
#    except:
#        pass
    file_finder = re.compile('.*\.\w{1,4}$')
    try:
        if not indent:
            print '\n[+] Pring Links from BeautifulSoup'
        soup = BeautifulSoup(html)
        links = soup.findAll(name='a')
        for link in links:
            if link.has_key('href'):
                output = link['href']
                if '../' in output:
                    continue
                print indentation + output
                if len(file_finder.findall(output)):
                    continue
                #if output.endswith('.mkv') or output.endswith('.jpg')\
                #        or output.endswith('mp4') or output.endswith('png')\
                #        or output.endswith('jpeg') \
                #        or output.endswith('avi') \
                #        or output.endswith('aac'):
                #    continue
                printLinks(url+'/'+output, indent=indent+1, ab=ab)
    except Exception, e:
        #print e
        pass
def main():
    parser = optparse.OptionParser('usage%prog ' +\
            '-u <target url>')
    parser.add_option('-u', dest='tgtURL', type='string',\
            help='specify target url')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    use_tor()
    if url == None:
        print parser.usage
        exit(0)
    else:
        printLinks(url)

if __name__=='__main__':
    main()
