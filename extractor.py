# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 14:41:22 2019

@author: ASUS
"""

from extract_features import extractor
import json
import urllib

class extractor2(extractor):
    def __init__(self):
        super().__init__()
        
    def extractLastLayer(self,lines):
        df=self.process(lines)
        store=[]
        for i in df:
            tem=json.loads(i)
            temStore=[]
            for feat in tem['features']:
                token=feat['token']
                layers=feat['layers']
                lastLayer=layers[0]
                try:
                    assert(lastLayer['index']==-1)
                except:
                    print(token)
                lastLayerVals=lastLayer['values']
                temStore.append({'token':token, 'values':lastLayerVals})
            store.append(temStore)
        return store
    
class squadExtractor():
    def __init__(self, devFName='', trainFName=''):
        if devFName=="":
            self.devFName, self.trainFName = self.downloadSquad()
        else:
            self.devFName=devFName
            self.trainFName=trainFName
            
    def downloadSquad(self):
        squadDev='squad/dev-v2.0.json'
        squadTrain='squad/train-v2.0.json'
        
        squadDevURL='https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json'
        squadTrainURL='https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json'
        
        urllib.request.urlretrieve(squadDevURL, squadDev)
        urllib.request.urlretrieve(squadTrainURL, squadTrain)
        return  squadDev, squadTrain
        
    def extractJson(self, fname):
        lst=[]
        for line in open(fname, 'r'):
            lst.append(json.loads(line))
        
        return lst
    
    def extractSquadJson(self, fname):
        dataStack=[]
        data=self.extractJson(fname)[0]['data']
        for compilation in data:
            paragraphs=compilation['paragraphs']
            for para in paragraphs:
                context=para['context']
                qas=para['qas']
                for question in qas:
                    quest=question['question']
                    answers=question['answers']
                    for ans in answers:
                        ansText=ans['text']
                        ansStart=ans['answer_start']
                        tem={
                            'context': context,
                            'question':quest,
                            'ansText': ansText,
                            'ansStart': ansStart
                                }
                        dataStack.append(tem)
        return dataStack
    
    def extractSquad(self, dataset='dev'):
        if dataset=='dev':
            fname=self.devFName
        else:
            fname=self.trainFName
        dev=self.extractSquadJson(fname)
        return dev
        
        
#lines=[]
#lines.append('jim henson was a puppeteer ||| hello testing')
#lines.append('jim henson was a puppeteer ||| hello testing')
#
#extract=extractor2()
#store=extract.extractLastLayer(lines)
#
#squadDev='squad/dev-v2.0.json'
#squadTrain='squad/train-v2.0.json'
#squadExtract=squadExtractor(squadDev, squadTrain)
#
#data=squadExtract.extractSquad()