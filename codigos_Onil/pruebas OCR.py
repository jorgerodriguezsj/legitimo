# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:19:55 2020

@author: Jorge
"""

from tesserocr import PyTessBaseAPI

images = ['prueba.jpg']

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(img)
        # print(api.GetUTF8Text())
        a=api.GetUTF8Text()
        print(api.AllWordConfidences())
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.


import tesserocr
from PIL import Image

print(tesserocr.tesseract_version())  # print tesseract-ocr version
print(tesserocr.get_languages())  # prints tessdata path and list of available languages

image = Image.open('1.jpg')
print(tesserocr.image_to_text(image))  # print ocr text from image
# or
print(tesserocr.file_to_text('1.jpg'))


from PIL import Image
from tesserocr import PyTessBaseAPI, RIL


with PyTessBaseAPI() as api:
    api.SetImage(image)
    boxes = api.GetComponentImages(RIL.TEXTLINE, True)
    print('Found {} textline image components.'.format(len(boxes)))
    for i, (im, box, _, _) in enumerate(boxes):
        # im is a PIL image object
        # box is a dict with x, y, w and h keys
        api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
        ocrResult = api.GetUTF8Text()
        conf = api.MeanTextConf()
        print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
              "confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))
        
        
        
from PIL import Image
from tesserocr import PyTessBaseAPI, PSM

with PyTessBaseAPI(psm=PSM.AUTO_OSD) as api:
    
    api.SetImage(image)
    api.Recognize()

    it = api.AnalyseLayout()
    orientation, direction, order, deskew_angle = it.Orientation()
    print("Orientation: {:d}".format(orientation))
    print("WritingDirection: {:d}".format(direction))
    print("TextlineOrder: {:d}".format(order))
    print("Deskew angle: {:.4f}".format(deskew_angle))
    
    
    
from tesserocr import PyTessBaseAPI, PSM, OEM

with PyTessBaseAPI(psm=PSM.OSD_ONLY, oem=OEM.LSTM_ONLY) as api:
    api.SetImageFile("1.jpg")

    os = api.DetectOrientationScript()
    print("Orientation: {orient_deg}\nOrientation confidence: {orient_conf}\n"
          "Script: {script_name}\nScript confidence: {script_conf}".format(**os))
    
    
from __future__ import print_function

from tesserocr import PyTessBaseAPI, RIL, iterate_level

with PyTessBaseAPI() as api:
    api.SetImageFile('1.jpg')
    api.SetVariable("save_blob_choices", "T")
    api.SetRectangle(37, 228, 548, 31)
    api.Recognize()

    ri = api.GetIterator()
    level = RIL.SYMBOL
    for r in iterate_level(ri, level):
        symbol = r.GetUTF8Text(level)  # r == ri
        conf = r.Confidence(level)
        if symbol:
            print(u'symbol {}, conf: {}'.format(symbol, conf), end='')
        indent = False
        ci = r.GetChoiceIterator()
        for c in ci:
            if indent:
                print('\t\t ', end='')
            print('\t- ', end='')
            choice = c.GetUTF8Text()  # c == ci
            print(u'{} conf: {}'.format(choice, c.Confidence()))
            indent = True
        print('---------------------------------------------')