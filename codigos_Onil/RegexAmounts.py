# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:52:38 2020

@author: Jorge
"""

"""
Extracted text from Total_amount, VAT, Amount_before_taxes y Witholding_tax
"""
#Some examples
test_str = ("27,37 €\n"
	"27,37€\n"
	"27,37 EUR\n"
	"1.230,11€\n"
	"1.230,11 €\n"
	"1.230€\n"
	"1.23 €\n"
	"1.350.230,25€\n"
	"1.350.230,25 €\n"
	"2,268.32€\n"
	"393.66€\n"
    "1,964.47€")


"""
First step

Extract only the numerical data, avoiding € or EUR
"""

import re

regex = r"[0-9.,]+"

matches = re.finditer(regex, test_str)
data = []
for match in matches:
    data.append(match.group())

"""
Second step

Function that formats the text and returns the new standar text
"""

def formateo(string):
    n_coma = string.count(',')  
    n_punto = string.count('.')
    if n_coma == 0:
        if len(string.split('.')[1]) > 2:
            string = string.replace('.','')
        else:
            string = string.replace('.',',')
        return string
    if n_punto == 0:
        return string    
    if n_coma != n_punto:
        if n_coma > n_punto:
            string = string.replace(',','').replace('.',',')
            return string
        if n_punto > n_coma:
            string = string.replace('.','')
            return string
    if n_coma == n_punto:
        pos_coma = string.find(',')
        pos_punto = string.find('.')
        if pos_punto < pos_coma:
            string = string.replace('.','')
            return string
        if pos_punto > pos_coma:
            string = string.replace(',','').replace('.',',')
            return string
            

for string in data:
    out = formateo(string) 
    print(string, ' -> ', out)

