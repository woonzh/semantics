# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 14:31:39 2018

@author: ASUS
"""

import json
import extractor

    
#lines=[]
#lines.append('jim henson was a puppeteer. hello testing')
#
#extract=extractor.extractor2()
#store=extract.extractLastLayer(lines)

squadDev='squad/dev-v2.0.json'
squadTrain='squad/train-v2.0.json'
squadExtract=extractor.squadExtractor(squadDev, squadTrain)

data=squadExtract.extractSquad()

chosen=data[130]
lines=[chosen['context']]
ans=chosen['ansText']
start=chosen['ansStart']
extract=extractor.extractor2()
store=extract.extractLastLayer(lines)