# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:45:06 2020

@author: Jorge
"""

import pytesseract
import cv2

def extraer_texto(image):
    """
    Parameters
    ----------
    imagen : CV image
       
    Returns
    -------
    text : DataFrame
        A dataframe with all the information extracted from the image with OCR
    string : String
        A string with only the text extracted from the image with OCR

    """

    # img = cv2.imread(image,0) #carga de la factura en .jpg
    img = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_data(img, lang='eng', nice=0, output_type='data.frame')
    text = text.dropna()
    text = text.reset_index()
    text = text.drop(columns=['level','page_num', 'block_num', 'par_num', 'line_num', 'word_num','index'])
    string = pytesseract.image_to_string(img,lang='eng')
    return text, string

image = '236.jpg'
img = cv2.imread(image,0) #carga de la factura en .jpg
text, string  = extraer_texto(img)