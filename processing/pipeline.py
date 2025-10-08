#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'

"""
Pipeline for processing various file types using optional segmentation and encoding using a semantic similarity model.

Supported file types and their processing modules are:

- CCP constitution XML files: process_constitutions.py
- Text documents of various types: process_documents.py
- Excel files: process_xlsx.py
- CSV files: process_csv.py

The core file set is CCP constitutions. Other corpora are provided to illustrate the processing of other file types, segmentation,
and multilingual capabilities.

spaCy English and Spanish language models are used for text segmentation. Various version of the models are provided. 
Segmentation is not supported for constitution XML

Google Universal Sentence Encoders (USE v4 for English, USE multilingual v3 for Spanish) provide encoding of text segments.

Configuration dictionaries supply the following fields for all file types:

'run': True|False. True if want to run processor else false
'processor': Processor module name. The processor .py file must be imported.
'data_path': Path to source files containing text to be segmented and encoded.
'model_path': Path to destination of segments, encodings, and supporting files.
'encoder_path': Path to encoder.
'spacy_path': Path to spaCy model used for segmentation.
'label': Name of process.
'description':Description of process.

The configuration for CCP XML files contain this customisable field:
'element_types': ['body','list'] which define the XML elements containing the text sections that are encoded.

The configurations for CCP XML files contain these customisable fields:
'data_fields': A list of names of columns that contain text to process.
'id_field': The column name to use as a row identifier. If empty or missing the row number is used.

NOTE: Excel and CSV fields must contain a header row containing column names.

"""

import process_constitutions
import process_ontology

from packages import *
from utilities import build_topic_segments_matrix

def main(config):

    print(f"Processing constitutions\n")
    segment_encodings = config['constitutions']['processor'].process(config)

    print(f"Processing ontotogy\n")
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
