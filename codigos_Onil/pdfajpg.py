# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:53:53 2020

@author: Jorge
"""

from wand.image import Image as wi
from pathlib import Path
from PIL import Image
import os
from wand.color import Color

path = '/Users/Legitimo/Desktop/Facturas_jpg'
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index+1), '.jpg'])))
    

def ls3(path):
    return [obj.name for obj in Path(path).iterdir() if obj.is_file()]

files = ls3(r'C:\Users\Legitimo\Desktop\pdf')
j=1
for dire in files:
    pdf = wi(filename=dire, resolution=300)
    pdf.compression_quality = 99
    pdf.background_color = Color("white")
    pdf.alpha_channel = 'remove'
    pdfimage = pdf.convert("jpeg")
    
    i=1
    for img in pdfimage.sequence:
        page = wi(image=img,resolution=300)
        page.background_color = Color("white")
        page.alpha_channel = 'remove'
        page.resize(1654,2337)
        page.save(filename=r"C:\Users\Legitimo\Desktop\jpgs\\"+ str(j) + str(i)+".jpg")
        i +=1
    j=j+1

pdf = wi(filename='BIYAK.pdf', resolution=300)
pdf.compression_quality = 95
pdf.background_color = Color("white")
pdf.alpha_channel = 'remove'
pdfimage = pdf.convert("jpeg")
pdfimage.background_color = Color("white")
pdfimage.alpha_channel = 'remove'
pdfimage.resize(1654,2337)
pdfimage.save(filename=r"C:\Users\Legitimo\Desktop\jpgs\\"+'biyak'+".jpg")

