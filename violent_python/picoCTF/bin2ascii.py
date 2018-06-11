def bin2ascii(num):
    hex = ""
    while num > 0:
        rem = num % 16
        num = num // 16
        hex = "%x"%rem + hex
    i = 0
    print hex
    out = ""
    while i < len(hex):
        out += "%c"%int(hex[i:i+2], 16)
        i+=2
    return out
def ascii2dec(text):
    out = ""
    for c in text:
        print c
        out += "%d"%ord(c)
    return out

def ascii2hex(text):
    out = ""
    for c in text:
        print c
        out += "%x"%ord(c)
    return out

def hash(text):
    result = 0
    for c in text:
        result += ord(c)
    result = result % 16
    print result

num = 0b0111000001101100011000010110100101100100
ascii = bin2ascii(num)
print ascii
print ascii2dec(ascii)
ascii = '1a558acddabd64bbccdd94903eafdf18'
print ascii2hex(ascii)
