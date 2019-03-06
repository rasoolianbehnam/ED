import os
try:
    import wx
    print("wx is installed")
except:
    os.system('pip install wxpython')

try:
    import cv2
    print("cv2 is installed")
except:
    os.system('pip install opencv-python')

os.system("pythonw ./show_images.py")
