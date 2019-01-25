#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:21:25 2019

@author: zhenhao
"""

import extractor
import tokenization

extract=extractor.extractor2()

a='text '*500

encodings=extract.extractLastLayer([a])[0]