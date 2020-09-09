# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:20:21 2020

@author: Jorge
"""
import xml.etree.ElementTree as ET
import pandas
import cv2
import pytesseract
from extraer_cif import extraer_CIF_NIF
import numpy as np

img_path = '298.jpg'
CIFin = 'B95883211'
tipo_factura = 1
# tipo_factura = 2


image = cv2.imread(img_path, 0)
cif_df = extraer_CIF_NIF(image,CIFin,tipo_factura)
print(cif_df)


if tipo_factura == 1:
    template_name = cif_df[cif_df.Clase == 'Sellers_VAT'].text.values[0]
if tipo_factura == 2:
    template_name = cif_df[cif_df.Clase == 'Buyers_VAT'].text.values[0]


estructura_xml = ET.parse(template_name + '.xml')

thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
tol = 2
df_cols = ["xmin", "ymin", "xmax","ymax", "conf", "text", "Clase"]
filas = []

for node in estructura_xml.iter('object'):
    name = node.find('name').text
    for subnode in node.iter('bndbox'):
        xmin = int(subnode.find('xmin').text if subnode is not None else None)-tol
        ymin = int(subnode.find('ymin').text if subnode is not None else None)-tol
        xmax = int(subnode.find('xmax').text if subnode is not None else None)+tol
        ymax = int(subnode.find('ymax').text if subnode is not None else None)+tol
        ROI = thresh[ymin:ymax,xmin:xmax]
        texto = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        text = pytesseract.image_to_data(ROI,lang='eng',config='--psm 6' ,output_type='data.frame')
        text = text.dropna()
        conf = int(text.conf.mean())
                
    filas.append({"xmin": xmin, "ymin": ymin, "xmax":xmax,"ymax":ymax, 
                  "conf": conf, "text": texto, "Clase": name})
       

df = pandas.DataFrame(filas, columns = df_cols)

image = cv2.imread(img_path)
n_boxes = len(df['text'])
for i in range(n_boxes):
    label = df.iloc[i]['Clase']
    color = list(np.random.random(size=3) * 256)
    (xmin, ymin, xmax, ymax) = (df.iloc[i]['xmin'], df.iloc[i]['ymin'], df.iloc[i]['xmax'], df.iloc[i]['ymax'])
    cv2.rectangle(image, (xmin, ymin), (xmax , ymax ), color, 2)
    cv2.putText(image,label,(xmax, ymin + int((ymax-ymin)/2)),cv2.FONT_HERSHEY_COMPLEX,0.5,color,2)
cv2.imwrite('bboxesimg.jpg', image)

