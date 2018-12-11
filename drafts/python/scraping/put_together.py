import os, sys

start = 1
last = 11131
pieces = 10
intervals = (last - start)//10

#for i in range(pieces):
#    a = "seg-{%d..%d}-v1-a1.jpg"%(i*intervals, i*intervals+intervals)
#    command = "cat %s | ffmpeg -i - -vcodec copy -acodec copy -bsf:a aac_adtstoasc -y out_%d.mp4"%(a, i)
#    os.system(command)

command = "cat out_{0..9}.mp4 | ffmpeg -i - -vcodec copy -acodec copy -bsf:a aac_adtstoasc -y out.mp4"
print command
os.system(command)
