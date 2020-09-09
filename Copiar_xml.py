# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:10:26 2020

@author: Jorge
"""

import shutil

intervalo = list(range(169, 175 +1))

for i in intervalo:
    shutil.copy('19.xml', str(i) + ".xml")