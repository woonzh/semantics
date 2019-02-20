#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:37:01 2019

@author: zhenhao
"""

extract_features.py -> contains main extractor to get the last layer of the bert encodings
extractor.py -> uses extractor in extract_features to create one for squad / extract, download squad dataset
squadProcessor.py -> uses classes in extractor to get the data we need for qa training. To store into interim folder
squad_trainer -> to use the processed data from squadProcessor to train qa