# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:03:07 2020

@author: Jorge
"""
import urllib.request
import xml.etree.ElementTree as ET
import os
from PIL import Image

path = r'C:\Users\Legitimo\Desktop\descargas_NNN'
files = os.listdir(path)

for archivo in files:
    tree = ET.parse(r'C:\Users\Legitimo\Desktop\descargas_NNN\\' + str(archivo))
    root = tree.getroot()
    root[0].text
    r= urllib.request.urlopen(root[0].text)
    f = open(str(os.path.splitext(archivo)[0]) + '.jpeg', "wb") 
    f.write(r.read()) 
    f.close()
    img = Image.open((os.path.splitext(archivo)[0]) + '.jpeg')
    new_img = img.resize((1654,2337))
    new_img.save((os.path.splitext(archivo)[0]) + '.jpeg','jpeg')
