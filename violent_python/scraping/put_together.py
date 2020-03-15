import os
import sys
from glob import glob
pattern, output, *_ = sys.argv[1:]
args = ' '.join(sorted(glob("*jpg"), key=lambda x: int(x.split("-")[1])) )
command = "cat %s | ffmpeg -i - -vcodec copy -acodec copy -bsf:a aac_adtstoasc -y out.mp4"%args
os.system(command)
