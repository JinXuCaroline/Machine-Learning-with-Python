#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from collections import Counter
import pandas as pd
from pandas import ExcelWriter
import string
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from nltk.stem.porter import PorterStemmer
from nltk.util import ngrams

# read json file
news = []
with open('News_Category_Dataset_v2.json') as news_category:
    for line in news_category:
        news.append(json.loads(line))
        
# create an excel workbook
workbook = ExcelWriter('News_Category_Analysis_try.xlsx')

# split and process text
def clean(col, n):
    elements = []
    ngrams_sum = []
    for i in news:
        for p in col:
            elements.append(i[p]) # extract contents from specific columns
    for j in elements:
        tokens = j.split(" ") # split
        token_lower = [w.lower() for w in tokens] #lower case
        # remove all the punctuations
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in token_lower]
        words = [word for word in stripped if word.isalpha()]        
        # filter out stop words
        stop_words = set(stopwords.words('English'))
        words_nostop = [w for w in words if not w in stop_words]
        # stemming of words
        porter = PorterStemmer()
        word_final = [porter.stem(word) for word in words_nostop]
        output_ngrams = list(ngrams(word_final, n))
        print(output_ngrams)
        ngrams_sum.extend(output_ngrams)
    count = Counter(ngrams_sum) # count frequency
    countDF = pd.DataFrame.from_dict(count, orient = 'index').reset_index()
    
    countDF.to_excel(workbook, "gram" + str(n))
    workbook.save()    
        

clean(["short_description","headline"],2 )
#clean(["short_description","headline"],2)










    
    