# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:54:49 2020

@author: Jorge
"""

import re

regex = r"(?:A|B|C|D|E|F|G|H|J|K|L|M|N|P|Q|R|S|U|V|W|X|Y|Z|\d){1}(?:[^a-zA-Z0-9_,\/°:]\s?\d{2}[^a-zA-Z0-9_,:]|[^a-zA-Z0-9_,\/°:]?\s?\d{2}[^a-zA-Z0-9_,\/:]?)(?:\d{3}[^a-zA-Z0-9_,\/-:]?\d{2}\w|\d{2}[^a-zA-Z0-9_,\/-:]?\d{2}[^a-zA-Z0-9_,\/.-:]?\d{2})\b"

test_str = ("A12345678\n"
	"B12345678\n"
	"C12345678\n"
	"D12345678\n"
	"E12345678\n"
	"F12345678\n"
	"G12345678\n"
	"H12345678\n"
	"J12345678\n"
	"U12345678\n"
	"V12345678\n\n"
	"N1234567L\n"
	"P1234567L\n"
	"Q1234567L\n"
	"R1234567L\n"
	"S1234567L\n"
	"W1234567L\n\n"
	"79009541X\n"
	"K9009541X\n"
	"L9009541X\n"
	"M9009541X\n"
	"X9009541X\n"
	"Y9009541X\n"
	"Z9009541X")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))