#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'

"""
Pipeline for processing:
1. In-force national constitutions from the CCP corpus. Constitutions are in XML format.
2. The CCP ontotogy of topics in a CSV.

Google's Universal Sentence Encoders v4 provides encoding of constitution text segment and topics.

Configuration dictionaries supply data required to process constitutions and topics.

This file outputs a topic-segment semantic similarity matrix.

"""

import process_constitutions
import process_ontology

from packages import *
from utilities import build_topic_segments_matrix

def main(config):

    print(f"\nProcessing constitutions\n")
    segment_encodings = config['constitutions']['processor'].process(config)

    print(f"\nProcessing ontotogy\n")
    topic_encodings = config['ontology']['processor'].process(config)
    
    # Build the topic-segment matrix
    topic_segment_matrix = build_topic_segments_matrix(topic_encodings,segment_encodings)
    filename = config['shared']['model_path'] +'topic_segment_matrix.json'
    with open(filename, 'w') as f:
        json.dump(np.array(topic_segment_matrix).tolist(), f)

    print('All done')

if __name__ == '__main__':

    config = {}

    config['shared'] = {
        'data_path': '../data/',
        'model_path': '../model/',
        'encoder_path': '../use-4/',
    }

    # Configuration for processing constitutions XML and CCP ontology
    config['constitutions'] = {
        'processor': process_constitutions,
        'constitutions_path': 'constitutions_xml/',
        'element_types': ['body','list'], # The XML elements we are processing
        'metadata_file': 'metadata.csv'
    }

    config['ontology'] = {
        'processor': process_ontology,
        'ontology_file': 'revised_ontology.csv',
        'key_field':'Key',
        'label_field':'Label',
        'description_field':'Description'
    } 

    main(config)
