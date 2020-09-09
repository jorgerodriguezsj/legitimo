# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:32:30 2020

@author: Jorge
"""

# Import libraries
import pandas as pd
import pytesseract as pt


# Read a pdf file as image pages
#pages = pdf2image.convert_from_path(pdf_path='files\\spcs-ob-893.pdf', dpi=200, size=(1654,2340))
image = 'prueba.jpg'
# Convert a page to a data frame (page 2)
ds = pt.image_to_data(image, lang='eng', nice=0, output_type='data.frame')

# Remove unnecessary columns in the data set
ds = ds.drop(columns=['level','page_num', 'block_num', 'par_num', 'line_num', 'word_num'])

# Sort data set top-to-down and left-to-right
ds = ds.sort_values(by=['top', 'left'], ascending=True)

# Create a bounding box around invoice number (Fakturanummer)
box = [418,386,530,403]

# Create a string
output = ''

# Loop data set and get contents inside the bounding box
for index, row in ds.iterrows():
    xmin = row['left']
    ymin = row['top']
    xmax = row['left'] + row['width']
    ymax = row['top'] + row['height']
    if(xmin >= box[0] and ymin >= box[1] and xmax <= box[2] and ymax <= box[3]):
        output += row['text']

# Print contents
print('Invoice number is: {0}'.format(output))

# Convert data frame to csv
ds.to_csv('files\\spcs-ob-893_p1.csv', index=False)




import pytesseract
from pytesseract import Output
import cv2
img = cv2.imread('2.jpg')

d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='spa+eng')
d = d.drop(columns=['level','page_num', 'block_num', 'par_num', 'line_num', 'word_num'])
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)


for i in range(n_boxes):
    if 'C.I.F' in d['text'][i]:
       print(d['text'][i+1])
       
       
       
       
       
       
import re
img = cv2.imread('2.jpg')
text = pytesseract.image_to_string(img,lang='spa+eng')       
re.search('[A-Z]{1}\d{8}', text).group()
re.findall('[A-Z]{1}\d{8}',text)       
       
       
