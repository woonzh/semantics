# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 14:31:39 2018

@author: ASUS
"""

import extractor
from storer import pickleStorer
import argparse
import tokenization
import time
import pandas as pd
import time

squadDev='squad/dev-v2.0.json'
squadTrain='squad/train-v2.0.json'

extract=extractor.extractor2()
squadExtract=extractor.squadExtractor(squadDev, squadTrain)
tokenizer = tokenization.FullTokenizer
longQAs=[]

fstorer=pickleStorer()

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
#            print(token)
            encodings[counter]['start']=True
            startFound = True
        else:
            encodings[counter]['start']=False
        
        if newEndIndex < 0 and endFound==False:
#            print(token)
            encodings[counter]['end']=True
            endFound=True
        else:
            encodings[counter]['end']=False
    
    return encodings

def batchedGetStartAndEnd(batch):
#    extract=extractor.extractor2()
    textStore=[]
    ansStore=[]
    startStore=[]
    questTextStore=[]
    questStore=[]
    for line in batch:
        textStore.append(line['context'])
        ansStore.append(line['ansText'])
        startStore.append(line['ansStart'])
        questStore.append(line['question'])
        questTextStore.append(line['question']+' ||| ' + line['context'] )
        
#    print(questTextStore)
#    return questTextStore
    
    encodings=extract.extractLastLayer(questTextStore)
    
    newEncodings=[]
    
    for counter, encoding in enumerate(encodings):
        spaceCount=0
        for i in range(startStore[counter]):
            if textStore[counter][i]==' ':
                spaceCount += 1
        
        newStartIndex=startStore[counter]-spaceCount
    
        spaceCount=0
        for i in range(len(ansStore[counter])):
            if textStore[counter][newStartIndex+1+i]==' ':
                spaceCount+=1
                
        newEndIndex = newStartIndex+len(ansStore[counter])-spaceCount
        
        
        startFound=False
        endFound=False
        contextStart=False
        temEncoding=[]
        for counter2, encode in enumerate(encoding):
            token=encode['token']
            if token == '[SEP]':
                contextStart=True
                
            if contextStart:
                if token != '[CLS]' and token != '[SEP]':
                    tokennew=token.replace('#','')
                    length=len(tokennew)
                    newStartIndex-=length
                    newEndIndex-=length
                    
                if newStartIndex < 0 and startFound==False:
#                    print(token)
                    encode['start']=True
                    startFound = True
                else:
                    encode['start']=False
                
                if newEndIndex < 0 and endFound==False:
#                    print(token)
                    encode['end']=True
                    endFound=True
                else:
                    encode['end']=False
                    
#                encode['text']= textStore[counter]
#                encode['ans']= ansStore[counter]
#                encode['question']= questTextStore[counter]
                temEncoding.append(encode)
                
        if endFound == False:
            longQAs.append({'text':textStore[counter], 'ans':ansStore[counter], 'question':questTextStore[counter]})
                    
        newEncodings.append({'encoding':temEncoding, 'text': textStore[counter], 'ans':ansStore[counter], 'question': questTextStore[counter]})
    
#    del extract
    del encodings
    return newEncodings, longQAs

def extractSquadBatch(dataset='dev', overwrite=False):
    if dataset=='dev':
        orgData=squadExtract.extractSquad()
    else:
        orgData=squadExtract.extractSquad('train')
    
    try:
        curStore, curLongQAs=fstorer.loadSquadEncoding(dataset)
        startId=len(curStore)
    except:
        startId=0
        
    batch_size=32
    processSize=30*batch_size
    
    data=orgData[startId:startId+processSize]
    
    count=0
    
    curTime=time.time()
    timeStore=pd.DataFrame(columns=['iteration', 'time'])
    
    while count < len(data):
        data_batch=data[count:min(count+batch_size, len(data))]
        newStore, newLongQAs=batchedGetStartAndEnd(data_batch)
        
        fstorer.store(newStore, newLongQAs, dataset)
        
        count+=batch_size
        timeStore.loc[len(timeStore)]=[len(timeStore), time.time()-curTime]
        print('%s iteration done in %s mins'%(len(timeStore), str((time.time()-curTime)/60)))
        curTime=time.time()
    
    timeStore.to_csv('squad/timings.csv')
    return store, longQAs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process squad files')
    parser.add_argument("datatype", default='dev', help='dataset type')
    parser.add_argument("overwrite", default='false', help='overwrite')
    
    args = parser.parse_args()
    
#    print(args.datatype)
#    print(args.overwrite)
    
    if args.overwrite=='true':
        overwrite=True
    else:
        overwrite=False
    
    start=time.time()
    store, longQAs=extractSquadBatch(args.datatype, overwrite)
    
    print("time taken: %s minutes"%(str(time.time()-start)/60))