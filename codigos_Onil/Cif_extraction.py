# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:20:12 2020

@author: Jorge
"""

import pytesseract
import re
import cv2
import pandas
import calendar
import locale
import datetime
from num2words import num2words

locale.setlocale(locale.LC_ALL, "es_ES")

def extraer_texto (imagen):
    """
    Parameters
    ----------
    imagen : Image path
       
    Returns
    -------
    text : DataFrame
        A dataframe with all the information extracted from the image with OCR
    string : String
        A string with only the text extracted from the image with OCR

    """
    img = cv2.imread(imagen,0) #carga de la factura en .jpg
    # thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_data(img, lang='eng', nice=0, output_type='data.frame')
    text = text.dropna()
    text = text.reset_index()
    text = text.drop(columns=['level','page_num', 'block_num', 'par_num', 'line_num', 'word_num','index'])
    string = pytesseract.image_to_string(img,lang='eng')
    return text, string
    
def extraer_CIF_NIF(text,string,CIFin,tipo_factura):
    """
    Parameters
    ----------
    text : DataFrame
        A dataframe with all the information extracted from the image with OCR
    string : String
        A string with only the text extracted from the image with OCR
    CIFin : String
        CIF or NIF of the seller or buyer according to the type of use that 
        is being given to the extraction (tipo_factura).
    tipo_factura : Integer
        tipo_factura = 1 #Facturas de proveedores
        tipo_factura = 2 #Facturas de ventas

    Returns
    -------
    cif_df : DataFrame
        Dataframe with all the information both positional and text of the 
        CIF / NIF found on the invoice.

    """
    
    cif = re.findall(r"(?:A|B|C|D|E|F|G|H|J|N|P|Q|R|S|U|V|W){1}(?:[^a-zA-Z0-9_,/°:]\s?\d{2}[^a-zA-Z0-9_,:]|[^a-zA-Z0-9_,/°:]?\s?\d{2}[^a-zA-Z0-9_,/:]?)(?:\d{3}[^a-zA-Z0-9_,/-:]?\d{2}\w|\d{2}[^a-zA-Z0-9_,/-:]?\d{2}[^a-zA-Z0-9_,/.-:]?\d{2})\b",string)
    
    for i in range(len(cif)):
        temptemp = cif[i].split(' ')
        idx = temptemp.index(max(temptemp, key=len))
        indice = text.loc[text.text.str.contains(temptemp[idx]),'text'].index.values[0] 
        tempdf = text[indice - idx : indice + (len(temptemp) - idx)]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
        
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['CIF']})
        text = text.append(df)
        text = text.drop(range(indice - idx , indice + (len(temptemp) - idx)))
        text = text.reset_index()
        text = text.drop(columns=['index']) 
    
    cif_df = text.dropna()
    cif_df['text'][:] = cif_df['text'][:].replace({'[.,/,—,-,),(]':''}, regex=True)
    cif_df = cif_df.reset_index().drop(columns=['index'])    
    
    if len(set(cif)) == 2:
        pass
    else:
        nif = re.findall(r'\b(?:\d|[KLMXYZ])\W?\d[-.,—]?\d{3}[-.,—]?\d{3}[-.,—_ ]?[A-Z]{1}\b',string)
        for i in range(len(nif)):
            temptemp = nif[i].split(' ')
            idx = temptemp.index(max(temptemp, key=len))
            indice = text.loc[text.text.str.contains(temptemp[idx]),'text'].index.values[0] 
            tempdf = text[indice - idx : indice + (len(temptemp) - idx)]
            left = tempdf.left.min()
            top = tempdf.top.max()
            width = tempdf.width.sum()
            height = tempdf.height.max()
            conf = int(tempdf.conf.mean())
            texto = tempdf.text.str.cat(sep=' ')
            
            df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                                   "conf": [conf], "text":[texto], "Clase":['CIF']})
            cif_df = cif_df.append(df)
            text = text.drop(range(indice - idx , indice + (len(temptemp) - idx)))
            text = text.reset_index()
            text = text.drop(columns=['index'])
            cif_df['text'][:] = cif_df['text'][:].replace({'[.,/,—,-,),(]':''}, regex=True)
            
            
    if len(cif_df)!= 0:
        cif_df['text'][:] = cif_df['text'][:].replace({'[.,/,—,-,),(]':''}, regex=True)
        cif_df = cif_df.reset_index().drop(columns=['index'])
        if tipo_factura == 1:
            for i in range(len(cif_df)):
                if cif_df.text.str.contains('.?'+ CIFin[3:9])[i]:
                    cif_df.Clase[i]='Buyers_VAT'
                else:
                    cif_df.Clase[i]='Sellers_VAT'
    
        if tipo_factura == 2:
            for i in range(len(cif_df)):
                if cif_df.text.str.contains('.?'+ CIFin[3:9])[i]:
                    cif_df.Clase[i]='Sellers_VAT'
                else:
                    cif_df.Clase[i]='Buyers_VAT'
                    
    if 'cif_df' in locals(): 
        pass
    else:
        cif_df = None 
        
        
    return  cif_df


imagen = '57.jpg' #Image path

CIFin = 'B26210559' #CIF or NIF of the seller or buyer according to the type of use that is being given to the extraction (tipo_factura).
# tipo_factura = 1 #Facturas de proveedores
tipo_factura = 2 #Facturas de ventas

text, string = extraer_texto(imagen)
cif_df = extraer_CIF_NIF(text,string,CIFin,tipo_factura)


"""
Simple code that draws bboxes in the input image
"""

tol = 5 #Tolerance parameter, which indicates how many pixels the original bbox enlarges in all dimensions

img = cv2.imread(imagen)
n_boxes = len(cif_df['text'])
for i in range(n_boxes):
    (x, y, w, h) = (cif_df.iloc[i]['left'], cif_df.iloc[i]['top'], cif_df.iloc[i]['width'], cif_df.iloc[i]['height'])
    cv2.rectangle(img, (x-tol, y-tol), (x + w +tol, y + h +tol), (255, 0, 0), 2)
    cv2.putText(imgcv,label,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
cv2.imwrite('bboxesimg.jpg', img)