import sys
import base64
coded_array = sys.stdin.read().split('\n')
#base64.b64decode(coded_string)
coded_string = ""
for line in coded_array[1:-2]:
    coded_string += line

print base64.b64decode(coded_string)
