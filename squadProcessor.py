# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 14:31:39 2018

@author: ASUS
"""

import extractor
import pickle
import argparse
import tokenization
import time
import pandas as pd

squadDev='squad/dev-v2.0.json'
squadTrain='squad/train-v2.0.json'

extract=extractor.extractor2()
squadExtract=extractor.squadExtractor(squadDev, squadTrain)
tokenizer = tokenization.FullTokenizer
longQAs=[]

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
                    print(token)
                    encode['start']=True
                    startFound = True
                else:
                    encode['start']=False
                
                if newEndIndex < 0 and endFound==False:
                    print(token)
                    encode['end']=True
                    endFound=True
                else:
                    encode['end']=False
                temEncoding.append(encode)
                
        if endFound == False:
            longQAs.append({'text':textStore[counter], 'ans':ansStore[counter], 'question':questTextStore[counter]})
                    
        newEncodings.append(temEncoding)
    
#    del extract
    del encodings
    return newEncodings

def loadSquadEncoding(dataset='dev'):
    if dataset=='dev':
        with open('squad/squadDev.p', 'rb') as f:
            a=pickle.load(f)
        with open('squad/longQAsDev.p', 'rb') as f:
            b=pickle.load(f)
    else:
        with open('squad/squadTrain.p', 'rb') as f:
            a=pickle.load(f)
        with open('squad/longQAsTrain.p', 'rb') as f:
            b=pickle.load(f)
    
    return a, b

def store(store, longQAs, dataset='dev', method='replace'):
    if method!='replace':
        try:
            curStore, curLongQAs=loadSquadEncoding(dataset)
            store=curStore+store
            longQAs=curLongQAs+longQAs
        except:
            print('no current storage found')
        
    if dataset=='dev':
        with open('squad/squadDev.p', 'wb') as f:
            pickle.dump(store, f)
        with open('squad/longQAsDev.p', 'wb') as f:
            pickle.dump(longQAs, f)
    else:
        with open('squad/squadTrain.p', 'wb') as f:
            pickle.dump(store, f)
        with open('squad/longQAsTrain.p', 'wb') as f:
            pickle.dump(longQAs, f)        
        

def extractSquadBatch(dataset='dev'):
    if dataset=='dev':
        orgData=squadExtract.extractSquad()
    else:
        orgData=squadExtract.extractSquad('train')
        
    temStore=[]
    batch_size=32
    
    data=orgData[0:100]
    
    count=0
    
    curTime=time.time()
    timeStore=pd.DataFrame(columns=['iteration', 'time'])
    
    while count < len(data):
        data_batch=data[count:min(count+batch_size, len(data))]
        temStore+=batchedGetStartAndEnd(data_batch)
        if len(data)<len(orgData) and count == 0:
            store(temStore, longQAs, dataset, 'add')
        else:
            store(temStore, longQAs, dataset)
        
        count+=batch_size
        timeStore.loc[len(timeStore)]=[len(timeStore), time.time()-curTime]
        curTime=time.time()
        print('%s iteration done.'%(len(timeStore)))
    
    timeStore.to_csv('squad/timings.csv')
    return store, longQAs

#df=extractSquadBatch()
#data=squadExtract.extractSquad()

def extractSquad(dataset='dev'):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process squad files')
    parser.add_argument("datatype", default='dev', help='dataset type')
    args = parser.parse_args()
    
    print(args.datatype)
    
    store, longQAs=extractSquadBatch(args.datatype)