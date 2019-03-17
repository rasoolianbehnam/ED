import os
try:
    import wx
except:
    os.system('pip install wxpython')

try:
    import cv2
except:
    os.system('pip install opencv-python')

os.system("pythonw show_images.py")
