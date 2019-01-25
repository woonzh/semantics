# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 14:31:39 2018

@author: ASUS
"""

import extractor
import pickle


squadDev='squad/dev-v2.0.json'
squadTrain='squad/train-v2.0.json'

extract=extractor.extractor2()
squadExtract=extractor.squadExtractor(squadDev, squadTrain)

def getStartAndEnd(orgText, orgStartIndex, ans):
    encodings=extract.extractLastLayer([orgText])[0]
    
    spaceCount=0
    for i in range(orgStartIndex):
        if orgText[i]==' ':
            spaceCount += 1
    
    newStartIndex=orgStartIndex-spaceCount
    
    spaceCount=0
    for i in range(len(ans)):
        if orgText[newStartIndex+1+i]==' ':
            spaceCount+=1
            
    newEndIndex = newStartIndex+len(ans)-spaceCount
    
    startFound=False
    endFound=False
    for counter, encode in enumerate(encodings):
        token=encode['token']
        if token != '[CLS]' and token != '[SEP]':
            tokennew=token.replace('#','')
            length=len(tokennew)
            newStartIndex-=length
            newEndIndex-=length
            
        if newStartIndex < 0 and startFound==False:
            print(token)
            encodings[counter]['start']=True
            startFound = True
        else:
            encodings[counter]['start']=False
        
        if newEndIndex < 0 and endFound==False:
            print(token)
            encodings[counter]['end']=True
            endFound=True
        else:
            encodings[counter]['end']=False
    
    return encodings

def extractSqaud(dataset='dev'):
    if dataset=='dev':
        data=squadExtract.extractSquad()
    else:
        data=squadExtract.extractSquad('train')
        
    store=[]
    
    for line in data:
        orgText=line['context']
        ans=line['ansText']
        start=line['ansStart']
        encoding=getStartAndEnd(orgText, start, ans)
        store.append(encoding)
        
    if dataset=='dev':
        with open('squad/squadDev.p', 'wb') as f:
            pickle.dump(store, f)
    else:
        with open('squad/squadTrain.p', 'wb') as f:
            pickle.dump(store, f)
    
    return store
        
def loadSqaudEncoding(dataset='dev'):
    if dataset=='dev':
        with open('squad/squadDev.p', 'rb') as f:
            a=pickle.load(f)
    else:
        with open('squad/squadTrain.p', 'rb') as f:
            a=pickle.load(f)
    
    return a

store=extractSqaud()