import sys
file_path = sys.argv[1]
file_name = file_path.split('/')[-1]
fd = open(file_path, 'rb')
dll_contents = fd.read()
fd.close()

print("[*] Filesize: %d" % len(dll_contents))

new_file_name = "%s:%s" % (sys.argv[2], file_name)
fd = open(new_file_name, 'wb')
print("[*] File saved as %s"%new_file_name)
fd.write(dll_contents)
fd.close()
