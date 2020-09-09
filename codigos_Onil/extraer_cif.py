# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:47:17 2020

@author: Jorge
"""

import re
import pandas
from extraer_texto import extraer_texto

def extraer_CIF_NIF(image,CIFin,tipo_factura):
    """
    Parameters
    ----------
    imagen : CV image
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
        
    text,string = extraer_texto(image)
    cif = re.findall(r"(?:A|B|C|D|E|F|G|H|J|N|P|Q|R|S|U|V|W){1}(?:[^a-zA-Z0-9_,/°:]\s?\d{2}[^a-zA-Z0-9_,:]|[^a-zA-Z0-9_,/°:]?\s?\d{2}[^a-zA-Z0-9_,/:]?)(?:\d{3}[^a-zA-Z0-9_,/-:]?\d{2}\w|\d{2}[^a-zA-Z0-9_,/-:]?\d{2}[^a-zA-Z0-9_,/.-:]?\d{2})\b",string)
    pandas.set_option('mode.chained_assignment', None) 
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
    cif_df['text'][:] = cif_df['text'][:].replace({'[-.,/—)(]':''}, regex=True)
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
            cif_df['text'][:] = cif_df['text'][:].replace({'[-.,/—)(]':''}, regex=True)
            
            
    if len(cif_df)!= 0:
        cif_df['text'][:] = cif_df['text'][:].replace({'[-.,/—)(]':''}, regex=True)
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
