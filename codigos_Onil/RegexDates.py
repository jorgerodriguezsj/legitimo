# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:59:30 2020

@author: Jorge
"""

import re
import calendar
import locale
from num2words import num2words
import datetime

#set locale 
locale.setlocale(locale.LC_ALL, "es_ES")

#Here I create a list with numbers written in letters. In the years you can put the desired range in rango_inf and rango_sup.
dias_letras = []
for i in range(1,32,1):
    dias_letras.append(num2words(i,lang='es'))

años_letras = []
rango_inf = 1950
rango_sup = 2050 + 1
for i in range(rango_inf,rango_sup,1):
    años_letras.append(num2words(i, lang='es'))

#Regex Patterns
regex1 = r"^(?:[1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])(?:.|\/|-|—|,){1}\s?(?:[1-9]|1[0-2]|0[0-9])(?:.|\/|-|—|,){1}(?:20[0-9][0-9]|9[0-9]|1[0-9]|0[0-9]|2[0-9])\b"
regex2 = r"^20[0-9][0-9](?:.|\/|-|—|,){1}(?:[1-9]|1[0-2]|0[0-9])(?:.|\/|-|—|,){1}(?:[1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])\b"
regex3 = r"^(?:[1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])\.?(?:\sde\s|\s)(?:%s)(?:\sde\s|\s)(?:2\.?0[0-9][0-9]|9[0-9]|1[0-9]|0[0-9]|2[0-9])\b" % '|'.join(calendar.month_name[1:])

#Here the problem with dot in month abbreviatures is fixed
abreviaturas = calendar.month_abbr[1:]
abr = []
for x in abreviaturas:
    abr.append(x.replace('.',''))
    
regex4 = r"^(?:[1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])[^a-zA-Z0-9_](?:%s)[^a-zA-Z0-9_]\s?(?:2\.?0[0-9][0-9]|9[0-9]|1[0-9]|0[0-9]|2[0-9])\b" % '|'.join(abr)
regex5 = r'(?:%s)' % '|'.join(dias_letras) + ' de (?:%s)' % '|'.join(calendar.month_name[1:]) + ' de (?:%s|20[0-9][0-9]|9[0-9]|1[0-9]|0[0-9]|2[0-9])$' % '|'.join(años_letras)

#Test sting, this string will be the one that the API returns in the date fields   
test_str = ("05.05.2020\n"
	"25/03/20\n"
	"30/06/2019\n"
	"04.05.20\n"
	"25-03-2020\n"
	"25—03—2020\n"
	"1/07/2017\n"
	"13/6/2017\n"
	"13,6,2017\n"
	"13,06,2017\n"
	"30/06/19\n\n"
	"2020/05/02\n"
	"2020-02-29\n"
	"2020—02—29\n\n\n"
	"20 de Marzo de 2020\n"
    "11 de febrero de 2020\n"
	"31 MARZO 2.020\n"
	"23 marzo 2020\n"
	"7. Mayo 2020\n"
	"01 de abril de 2020\n\n"
    "22 Oct. 16\n"
    "01 Ago. 15\n"
    "01 Ago 15\n"
    "19-Feb-2019\n"
    "19.Feb.2019\n"
    "19 Feb 2019\n"
    "19-Feb-19\n"
    "19.Feb.19\n\n"
    "Diecisiete de Mayo de Dos Mil Diecisiete\n"
    "Diecisiete de Mayo de 2017\n")

#To simplify the search we put the string in lowercase 
test_str = test_str.lower()

#With regex patterns we find the different matchs 
matches1 = re.finditer(regex1, test_str, re.MULTILINE)
matches2 = re.finditer(regex2, test_str, re.MULTILINE)
matches3 = re.finditer(regex3, test_str, re.MULTILINE)
matches4 = re.finditer(regex4, test_str, re.MULTILINE)
matches5 = re.finditer(regex5, test_str, re.MULTILINE)



fechas = [] #In this list we can find the extracted dates in standard format

#Datetime formats
formato1 = ['%d/%m/%Y','%d/%m/%y']
formato2 = ['%Y/%m/%d'] 
formato3 = ['%d de %B de %Y', '%d %B %Y']   
formato4 = ['%d %b %Y', '%d %b %y']     

d = [] #temporal list 
for match in matches1:
    d.append(match.group().replace('.','/').replace('-','/').replace(',','/').replace('—','/')) #Cleaning the string
for dat in d:
    for fmt in formato1:
        try:
            fechas.append(datetime.datetime.strptime(dat, fmt).date().strftime("%x")) #Save dates in fechas list in spanish standard format
        except:
            pass
d = []    
for match in matches2:
    d.append(match.group().replace('.','/').replace('-','/').replace(',','/').replace('—','/'))#Cleaning the string
for dat in d:
    for fmt in formato2:
        try:
            fechas.append(datetime.datetime.strptime(dat, fmt).date().strftime("%x"))  #Save dates in fechas list in spanish standard format
        except:
            pass

d = []          
for match in matches3:
    d.append(match.group().replace('.','')) #Cleaning the string
for dat in d:
    for fmt in formato3:
        try:
            fechas.append(datetime.datetime.strptime(dat, fmt).date().strftime("%x"))  #Save dates in fechas list in spanish standard format
        except:
            pass    

d = []      
temp = []
for match in matches4:
    d.append(match.group().replace('. ', ' ').replace('.',' ').replace('-',' ').replace(',',' ').replace('—',' ')) #Cleaning the string

#Here we have again problems with dot in abbreviatures, so we fix them
for j in range(len(d)):
    for i in range(len(abr)):
        if abr[i] in d[j]:
            temp.append(d[j].replace(abr[i],abreviaturas[i]))
d = temp      
for dat in d:
    for fmt in formato4:
        try:
            fechas.append(datetime.datetime.strptime(dat, fmt).date().strftime("%x"))  #Save dates in fechas list in spanish standard format
        except:
            pass    

d = []
temp = []        
for match in matches5:
    d.append(match.group().replace('.','/').replace('-','/').replace(',','/').replace('—','/')) #Cleaning the string

#Here we convert numbers in letters to integer using previously created lists    
for i in range(len(d)):
    a = d[i].split(' de ')
    for j in range(len(dias_letras)):
        if str(dias_letras[j]) == a[0]:
            a[0] = str(j+1)
    for j in range(len(años_letras)):
        if str(años_letras[j]) == a[2]:
            a[2] = str(j+rango_inf)
    d[i] = " ".join(a)
           
for dat in d:
    for fmt in formato3:
        try:
            fechas.append(datetime.datetime.strptime(dat, fmt).date().strftime("%x"))  #Save dates in fechas list in spanish standard format
        except:
            pass 



#Print results
    
print('Regex1')
for matchNum, match in enumerate(matches1, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
print('')
print('Regex2')        
for matchNum, match in enumerate(matches2, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
        
print('')
print('Regex3')        
for matchNum, match in enumerate(matches3, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

print('')
print('Regex4')        
for matchNum, match in enumerate(matches4, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
        
print('')
print('Regex5')        
for matchNum, match in enumerate(matches5, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))