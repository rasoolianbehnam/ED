import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
    def __init__( self, key, mode=AES.MODE_CBC):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()
        self.mode = mode

    def encrypt( self, raw ):
        raw = self.pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, self.mode, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, self.mode, iv )
        return self.unpad(cipher.decrypt( enc[16:] ))

    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

def print_in_hex(text):
    output = ""
    for c in text:
        output += "\\x%02x"%ord(c)
    return output

