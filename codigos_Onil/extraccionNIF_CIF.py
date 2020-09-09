# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:53:22 2020

@author: Jorge
"""

"""
Código que permite obtener el cif del vendedor mediante OCR en una factura
Necesita previamente introducir el cif del comprador
En la aplicación como el cliente va a ordenar las facturas en funcion de sus 
clientes se puede determinar su cif previamente.

Es decir, una consultoría ordena sus facturas por clientes, deberá introducir 
ese cif una vez por cada cliente para quedar así asignado
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
    img = cv2.imread(imagen) #carga de la factura en .jpg
    text = pytesseract.image_to_data(img, lang='eng', nice=0, output_type='data.frame')
    text = text.dropna()
    text = text.reset_index()
    text = text.drop(columns=['level','page_num', 'block_num', 'par_num', 'line_num', 'word_num','index'])
    string = pytesseract.image_to_string(img,lang='eng')
    # string = string.lower()
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
        CIF / NIF found on the invoice..

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


"""
FECHAS
"""

def extraer_fecha(text,string):
    
    text.text = text.text.str.lower()
    dias_letras = []
    
    for i in range(1,32,1):
        dias_letras.append(num2words(i,lang='es'))
        
    años_letras = []
    
    for i in range(1950,2051,1):
        años_letras.append(num2words(i, lang='es'))
    
    pandas.set_option('mode.chained_assignment', None)    
        
    temp = re.findall(r'[0-3][0-9][.,-,/,—]{1}[0-1][0-9][.,-,/,—]{1}\d{4}\b',text['text'].to_string()) 
    temp = temp + re.findall(r'\b\d{2}[.,-,/,—]{1}[0-1][0-9][.,-,/,—]{1}\d{2}\b',text['text'].to_string()) 
    temp = temp + re.findall(r'\b\d{4}[.,-,/,—]{1}[0-1][0-9][.,-,/,—]{1}\d{2}\b',text['text'].to_string())
    temp = temp + re.findall(r'\b\d{4}\-\d{2}\-\d{2}\b',text['text'].to_string())
    temp = temp + re.findall(r'\b\d{1}\.\d{1}\.\d{2}\b',text['text'].to_string()) 
    temp = temp + re.findall(r'\b\d{1}\.\d{1}\.\d{4}\b',text['text'].to_string())
    temp = temp + re.findall(r'\b\d{2}\-\d{2}\-\d{2}\b',text['text'].to_string()) 
    temp = temp + re.findall(r'\b\d{1,2}\-\d{2}\-\d{4}\b',text['text'].to_string())
    temp = temp + re.findall(r'\b\d{2}\/\d{1}\/\d{4}\b',text['text'].to_string())
    
    temp1 = re.findall(r'\b\d{2}[.,-,/,—]{1}\s[0-9][.,-,/,—]{1}\d{2}\b',string)
    for i in range(len(temp1)):
        temp1[i] = re.sub(' ','',temp1[i])
    temp = temp + temp1
    
    for i in range(len(temp)):
        text.loc[text.text.str.contains('.?'+ temp[i]),'Clase'] = 'Fecha' 
    
    temp1 = re.findall(r'\d{1,2} de (?:%s) de \d{4}\b' % '|'.join(calendar.month_name[1:]),string)
    
    for i in range(len(temp1)):
        temptemp = temp1[i].split(' ')
        indice = text.loc[text.text.str.contains('.?'+ temptemp[2]),'text'].index.values[0]
        tempdf = text[indice-2:indice+3]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
        
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['Fecha']})
        text = text.append(df)
        text = text.drop(range(indice-2,indice+3))
        text = text.reset_index()
        text = text.drop(columns=['index'])
        
    temp1 = re.findall(r"\d{2} (?:%s) \d.?\d\d\d\b" % '|'.join(calendar.month_name[1:]),string)
    
    for i in range(len(temp1)):
        temptemp = temp1[i].split(' ')
        indice = text.loc[text.text.str.contains('.?'+ temptemp[1]),'text'].index.values[0]
        tempdf = text[indice-1:indice+2]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
            
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['Fecha']})
        text = text.append(df)
        text = text.drop(range(indice-1,indice+2))
        text = text.reset_index()
        text = text.drop(columns=['index'])
        
    temp1 = re.findall(r'(?:%s)' % '|'.join(dias_letras) + 
                             ' de (?:%s)' % '|'.join(calendar.month_name[1:]) +
                             ' de (?:%s).*' % '|'.join(años_letras),string)
    for i in range(len(temp1)):
        temptemp = temp1[i].split(' ')
        mes = re.findall(r"(?:%s)\b" % '|'.join(calendar.month_name[1:]),temp1[i])
        idx = temptemp.index(mes[0])
        indice = text.loc[text.text.str.contains('.?'+ temptemp[idx]),'text'].index.values[0]
        tempdf = text[indice-idx:indice+(len(temptemp)-idx)]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
            
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['Fecha']})
        text = text.append(df)
        text = text.drop(range(indice-idx,indice+(len(temptemp)-idx)))
        text = text.reset_index()
        text = text.drop(columns=['index'])
    
    temp1 = re.findall(r'\d{1,2} (?:%s)\.? \d{1,4}\b' % '|'.join(calendar.month_abbr[1:]),string)
    
    for i in range(len(temp1)):
        temptemp = temp1[i].split(' ')
        mes = re.findall(r"(?:%s)\.?" % '|'.join(calendar.month_abbr[1:]),temp1[i])
        idx = temptemp.index(mes[0])
        indice = text.loc[text.text.str.contains('.?'+ temptemp[idx]),'text'].index.values[0]
        tempdf = text[indice-idx:indice+(len(temptemp)-idx)]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
                
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['Fecha']})
        text = text.append(df)
        text = text.drop(range(indice-idx,indice+(len(temptemp)-idx)))
        text = text.reset_index()
        text = text.drop(columns=['index'])
        
    temp1 = re.findall(r'\d*\d\.? (?:%s)\.? \d{1,4}\b' % '|'.join(calendar.month_name[1:]),string)
    
    for i in range(len(temp1)):
        temptemp = temp1[i].split(' ')
        mes = re.findall(r"(?:%s)\b" % '|'.join(calendar.month_name[1:]),''.join(temp1[i]))
        idx = temptemp.index(mes[0])
        indice = text.loc[text.text.str.contains(temptemp[idx]),'text'].index.values[0]
        tempdf = text[indice-idx:indice+(len(temptemp)-idx)]
        left = tempdf.left.min()
        top = tempdf.top.max()
        width = tempdf.width.sum()
        height = tempdf.height.max()
        conf = int(tempdf.conf.mean())
        texto = tempdf.text.str.cat(sep=' ')
        text = text.drop(range(indice-idx,indice+(len(temptemp)-idx)))
    
        df = pandas.DataFrame({"left":[left], "top":[top], "width":[width],"height":[height], 
                               "conf": [conf], "text":[texto], "Clase":['Fecha']})
        text = text.append(df)
        text = text.drop(range(indice-idx,indice+(len(temptemp)-idx)))
        text = text.reset_index()
        text = text.drop(columns=['index'])   
        
    temp = temp + re.findall(r'\d*\d\.? (?:%s)\.? (?:\d{4}\b|\d{2}\b(?!:\d))' % '|'.join(calendar.month_abbr[1:]),string)
    
    
    temp = temp + re.findall(r'\d{1,2}\s?\-\s?(?:%s)\s?\-\s?\d{1,4}\b' % '|'.join(calendar.month_abbr[1:]),string)
    
    
    for i in range(len(temp)):
        text.loc[text.text.str.contains('.?'+ temp[i]),'Clase'] = 'Fecha' 
              
    fecha_df = text.dropna()
    fecha_df = fecha_df[fecha_df['Clase'] == 'Fecha']
    fechas = []
    formatos = ['%d/%m/%Y','%d.%m.%Y','%d-%m-%Y','%d—%m—%Y',
                '%d/%m/%y','%d.%m.%y','%d-%m-%y','%d—%m—%y',
                '%Y/%m/%d','%Y.%m.%d','%Y-%m-%d','%Y—%m—%d',
                '%d de %B de %Y']
    
    for fecha in temp:
        for fmt in (formatos):
            try:
                fechas.append(datetime.datetime.strptime(fecha, fmt).date())
                # print(fecha + ' ' + fmt +' ok')
            except ValueError:
                # print(fecha + ' ' + fmt +' No')
                pass


       
    
    return fechas, temp ,fecha_df, text


imagen = '11.jpg'
CIFin = 'B95883211'
tipo_factura = 1 #Facturas de proveedores
# tipo_factura = 2 #Facturas de ventas

text, string = extraer_texto(imagen)
cif_df = extraer_CIF_NIF(text,string,CIFin,tipo_factura)
fechas,temp,fecha_df, text= extraer_fecha(text,string)







imagen = '11.jpg'
CIFin = 'B95883211'
text, string = extraer_texto(imagen)
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
           









































bboxes = cif_df.append(fecha_df)

tol = 10
img = cv2.imread(imagen)
n_boxes = len(bboxes['text'])
for i in range(n_boxes):
    (x, y, w, h) = (bboxes.iloc[i]['left'], bboxes.iloc[i]['top'], bboxes.iloc[i]['width'], bboxes.iloc[i]['height'])
    cv2.rectangle(img, (x-tol, y-tol), (x + w +tol, y + h +tol), (255, 0, 0), 2)
    cv2.putText(imgcv,label,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
cv2.imwrite('bboxesimg.jpg', img)
























from word2number import w2n

a = re.findall(r'\b(?:%s)' % '|'.join(dias_letrasM) + 
                         ' de (?:%s)' % '|'.join(m.title().rstrip('.') for m in calendar.month_name[1:]) +
                         ' de (?:%s).*' % '|'.join(m.title().rstrip('.') for m in años_letrasM),string)

b = a[0].split(' de ')

años = {'numero': list(range(1950,2051)), 'letra': años_letras}
años = pandas.DataFrame(años, columns = ['numero','letra'])
dias = {'numero': list(range(1,32)), 'letra': dias_letras}
dias = pandas.DataFrame(dias, columns = ['numero','letra'])

b[0]=b[0].lower()
b[0] = re.sub('[.,!@#$]', '', b[0])
idx = dias.index[dias['letra'] == b[0]]
b[0] = dias.loc[idx]['numero'].values[0]

b[2]=b[2].lower()
b[2] = re.sub('[.,!@#$]', '', b[2])
idx = años.index[años['letra'] == b[2]]
b[2] = años.loc[idx]['numero'].values[0]

a = str(b[0]) + ' de ' + b[1] + ' de ' + str(b[2])



a = r'(?:%s)' % '|'.join(dias_letrasM) + ' de (?:%s)' % '|'.join(m.title().rstrip('.') for m in calendar.month_name[1:]) + ' de (?:%s)' % '|'.join(m.title().rstrip('.') for m in años_letrasM)
    
a = r' de (?:%s) de \d{4}\b' % '|'.join(calendar.month_name[1:])

#DIbujar Bboxes en la imagen
# n_boxes = len(a['text'])
# for i in range(n_boxes):
#     (x, y, w, h) = (a.iloc[i]['left'], a.iloc[i]['top'], a.iloc[i]['width'], a.iloc[i]['height'])
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)

text = text.dropna()
tol = 10
img = cv2.imread(imagen)
n_boxes = len(fecha_df['text'])
for i in range(n_boxes):
    (x, y, w, h) = (fecha_df.iloc[i]['left'], fecha_df.iloc[i]['top'], fecha_df.iloc[i]['width'], fecha_df.iloc[i]['height'])
    cv2.rectangle(img, (x-tol, y-tol), (x + w +tol, y + h +tol), (255, 0, 0), 2)

cv2.imwrite('bboxesimg.jpg', img)

# cv2.imshow('img', img)
# cv2.waitKey(0)
