import sys
#text = '1a558acddabd64bbccdd94903eafdf18'
#text = 'ad6e2adecc04b88384cbc453229fc308c74d3ed758a294915ca48b6275fd3507bccfe2ccb19e8cc7fc7ca701b0a1f759'
##for c in text:
##    sys.stdout.write("0x%02d"%ord(c))
#
#i = 0
#while i < len(text)-2:
#    num = int(text[i:i+2], 16)
#    i += 2
#
#txt = text
#print(''.join([chr(int(''.join(c), 16)) for c in zip(txt[0::2],txt[1::2])]))
#
def ascii2hex(text):
    out = ""
    for c in text:
        out += "%02x"%ord(c)
    return out
text = '29R_$SR'
code = ascii2hex(text)
print code
