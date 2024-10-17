#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'

"""
Build and serialize topic dictionaries and encodings

"""
from packages import *

def process(data_path,encoder):
    topics_csv = []
    with open(data_path + 'revised_ontology.csv', 'r') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        for row in reader:
            topics_row = []
            topics_row.append(row[0])
            topics_row.append(row[5])
            topics_row.append(row[6])
            topics_csv.append(topics_row)
    topics_dict = {}
    encoded_topics = []
    topics = sorted(topics_csv, key=lambda x: x[0])
    text_list = []
    for row in topics:
        if len(row[0]) == 0:
            continue
        topics_dict[row[0]] = {}
        topics_dict[row[0]]['label'] = row[1]
        topics_dict[row[0]]['description'] = row[2]
      
        text = row[1] + '.'
        text += ' ' + row[2]
        text_list.append(text)
        encoded_topics.append(row[0]) 
    encodings = encoder(text_list)
    assert(len(encodings) == len(text_list))
    assert(len(encodings) == len(encoded_topics)) 
    return topics_dict,np.array(encodings).tolist(),encoded_topics
