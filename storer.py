#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:14:01 2019

@author: zhenhao
"""

import json
#import pickle
import _pickle as pickle
import pickle as pic

class storer:
    def __init__(self):
        self.jnames={
        'squadDev': 'squad/squadDev.json',
        'longqaDev': 'squad/longQAsDev.json',
        'squadTrain': 'squad/squadTrain.json',
        'longqaTrain': 'squad/longQAsTrain.json'
        }
        
        self.pnames={
        'squadDev': 'squad/squadDev.p',
        'longqaDev': 'squad/longQAsDev.p',
        'squadTrain': 'squad/squadTrain.p',
        'longqaTrain': 'squad/longQAsTrain.p',
        'tem':'squad/squadDev (copy).p'
        }
        
    def getfNames(self):
        return list(self.fnames)
    

class jsonStorer(storer):
    def __init__(self):
        super().__init__()
    
    def load(self,fname):
        with open(self.jnames[fname]) as f:
            store = json.load(f)
        return store
    
    def save(self, data, fname):
        with open(self.jnames[fname], 'w') as f:
            json.dump(data,f)
        return data
    
    def importFromPickle(self, pickleFName, fname):
        with open(pickleFName, 'rb') as f:
            a=pickle.load(f)
        data=self.save(a, fname)
        
class pickleStorer(storer):
    def __init__(self):
        super().__init__()
    
    def load(self,fname, complete=True, indexStart=0, indexEnd=0):
        store=[]
        with open(self.pnames[fname], 'rb') as f:
#            return pickle.load(f)
            if complete:
                store=[]
                try:
                    while True:
                        store.append(pickle.load(f))
                except EOFError:
                    pass
                return store
            else:
                counter=0
                store=[]
                while (counter <= indexEnd):
                    tem=pickle.load(f)
                    if counter >=indexStart:
                        store.append(tem)
                    counter+=1
                return store
    
    def save(self, data, fname, incremental=True):
        if incremental:
            with open(self.pnames[fname], 'ab') as f:
                pic.dump(data,f, pic.HIGHEST_PROTOCOL)
        else:
            with open(self.pnames[fname], 'wb') as f:
                pickle.dump(data,f)
    
    def loadSquadEncoding(self,dataset='dev'):
        if dataset=='dev':
            a=self.load('squadDev', True)
            b=self.load('longqaDev', True)
        else:
            a=self.load('squadTrain', True)
            b=self.load('longqaTrain', True)
        
        return a, b
    
    def store(self, store, longQAs, dataset, incremental=True):
        if dataset=='dev':
            self.save(store, 'squadDev', incremental)
            self.save(longQAs, 'longQAsDev', incremental)
        else:
            self.save(store, 'squadTrain', incremental)
            self.save(store, 'longQAsTrain', incremental)
            
    def restorePickle(self, orgfile, fname):
        df=self.load(orgfile)[0]
#        return df
        count=0
        for i in df:
            if count == 0:
                self.save(i, fname, False)
                count+=1
            else:
                self.save(i, fname, True)
        
#storer=jsonStorer()
#storerp=pickleStorer()
#storerp.restorePickle('tem', 'squadDev')
#df=storerp.load('squadDev', False)
#storer.importFromPickle('squad/squadDev.p', 'squadDev')
#tem=[{'a': 123, 'b':345}, {'c':134, 'd':4567}]
#
#storerp.save(tem, 'squadTrain', True)
#
#df=storerp.load('squadDev', True)