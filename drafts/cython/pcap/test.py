#from stdlib_test import *
import pcap

class mardas:
    text = ""
    def __init__(self, t):
        self.text = t
    def __add__(self, c):
        return "%s%s"%(self.text, c)
    def __len__(self):
        return len(self.text)

a = pcap.Pcap()
a.main()
