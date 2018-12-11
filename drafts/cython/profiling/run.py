import os, sys

filename_and_path = sys.argv[1]
filename = filename_and_path.split("/")[-1]
path = filename_and_path[:-len(filename)]
extension = filename.split(".")[-1]
basename = filename[:-len(extension)-1]

print " ".join(sys.argv)
if extension == "py":
    os.system("python %s"%(" ".join(sys.argv[1:])))
elif extension == "pyx" or extension == "pxd":
    os.system("python setup.py build_ext --inplace")
else:
    print "No suitable extension found"

