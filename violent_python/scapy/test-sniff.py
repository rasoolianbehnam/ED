from scapy.all import *
import re
def pktPrint(pkt):
    if pkt.haslayer(Dot11Beacon):
        print '[+] Detected 802.11 Beacon Frame'
    elif pkt.haslayer(Dot11ProbeReq):
        print '[+] Detected 802.11 Probe Request'
    elif pkt.haslayer(TCP):
        print '[+] Detected a TCP Packet'
        raw = pkt.sprintf("%Raw.load%")
        username = re.findall('(?i)user(.*)', raw)
        password = re.findall('(?i)pass(.*)', raw)
        if password:
            print '[*] Password found: %s, %s' % (username, password)
        
    elif pkt.haslayer(DNS):
        print '[+] Detected a DNS Packet'

def findGoogle(pkt):
    if pkt.haslayer(TCP):
        payload = pkt.sprintf('%Raw.load%')
        result = re.findall('facebook', payload)
        if result:
            print result
            r = re.findall(r'(?i)\&q=(.*)\&', payload)
            if r:
                search = r[0].split('&')[0]
                search = search.replace('q=', '').\
                        replace('+', ' ').replace('%20', ' ')
                print '[+] Searched For: ' + search
def credSniff(pkt):
    if pkt[TCP].payload:
        dest = pkt.getlayer(IP).dst
        raw = pkt.sprintf('%Raw.load%')
        user = re.findall('(?i)user(.*)', raw)
        pswd = re.findall('(?i)pass(.*)', raw)
        if user:
            print '[*] Detected Login to ' + str(dest)
            print '[+] User account: ' + str(user[0])
        elif pswd:
            print '[+] Password: ' + str(pswd[0])
def hiddenDot11(p):
    if p.haslayer(Dot11ProbeResp):
        addr2 = p.getlayer(Dot11).addr2
        if (addr2 in hiddenNets) & (addr2 not in unhiddenNets):
            netName = p.getlayer(Dot11ProbeResp).info
            print '[+] Decloaked Hidden SSID: %s for MAC: %s'\
                    %(netName, addr2)
            unhiddenNets.append(addr2)
    if p.haslayer(Dot11Beacon):
        info = p.getlayer(Dot11Beacon).info.replace(' ', '')
        addr2 = p.getlayer(Dot11).addr2
        if info == '' or ord(info[0]) == 0:
            if addr2 not in hiddenNets:
                hiddenNets.append(addr2)
                print '[-] Detected Hidden SSID with MAC:', addr2
        elif addr2 not in unhiddenNets:
            unhiddenNets.append(addr2)
            print '[+] Detected SSID with MAC: %s, %s'\
                    %(addr2, info)

conf.iface = 'wlx00c0ca92655b'
unhiddenNets= []
hiddenNets = []
sniff(prn=hiddenDot11)
