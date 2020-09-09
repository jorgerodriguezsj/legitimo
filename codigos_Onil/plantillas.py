# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 12:36:04 2020

@author: Jorge
"""
import re

funciones = ['fechap','cantidadp','cantidadn','fechan']
funcionestrad = ['_date_in_words','_amount_in_words','_amount_format','_sdate']

regex_corchetes = r"(?:[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\s|(?:%s)\((?:[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)\))" % '|'.join(funciones)
regex_dentro_corchetes = r"\{\{(.*?)\}\}"
regex1 = r"[a-zA-Z_]+\.[a-zA-Z_]+[0-9]?"
regex2 = r"loop\([a-zA-Z0-9_.]+\)"



texto = """
El abajo firmante firmante.nombre firmante.apellido1 que reside en firmante.domicilio solicita cantidadp(factura.fecha_fra) y holahola

Y aquí va otro parrafo en el que indico fechap(nada_interesante)
fechap(fecha_sustrae), loop(campeonato.equipo)
endfor
"""

#texto = str(para.text)
texto = texto.replace('endfor','{% endfor %}')
matches = re.finditer(regex_corchetes, texto)
for match in matches:
    var = str(match.group()).replace(' ','')
    texto = texto.replace(var,'{{' + var + '}}')

for i in range(len(funciones)):
    texto = re.sub(funciones[i],funcionestrad[i],texto)
    
matches = re.finditer(regex_dentro_corchetes,texto)

for matchNum, match in enumerate(matches, start=1):
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        text = match.group(groupNum)
        matches1 = re.finditer(regex1, text)
        for match in matches1:
            var = str(match.group())
            texto = texto.replace(var, var.split('.')[0] + '_form["' + var.split('.')[1] + '"]')

matches = re.finditer(regex2, texto)

for match in matches:
    var = str(match.group())
    var1 = var.replace('(','.').replace(')','')
    print(var1)
    
    texto = texto.replace(var,'{% for ' + var1.split('.')[1] + ' in ' + var1.split('.')[2] + ' %}')

    
       
print(texto)




    
matches = re.finditer(regex, texto)
for match in matches:
    var = str(match.group())
    print(var)
    texto = texto.replace(var,'{{' + var + '}}')
    #para.text = texto

    matches1 = re.finditer(regex1, texto)
    for match in matches1:
        var = str(match.group())
        print(var)
        texto = texto.replace(var, var.split('.')[0] + '_form["' + var.split('.')[1] + '"]')
        #para.text = texto
    for i in range(len(funciones)):
        texto = re.sub(funciones[i],funcionestrad[i],texto)
       # para.text = texto

matches = re.finditer(regex2, texto)
for match in matches:
    var = str(match.group())
    print(var)
    texto = texto.replace(var,'{% for ' + var.split('.')[1] + ' in ' + var.split('.')[2] + ' %}')
    #para.text = texto

print(texto)


