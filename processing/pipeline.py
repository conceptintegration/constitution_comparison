#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'


"""

Updated CCP processing based on:

1. XML files
2. Revised ontology


Data sources:

- constitutions_xml: a directory of CCP constitution XML files. File names provide the document IDs
- const_list.json: List of constitutions with metadata obtained from the constituteproject.org API.
  Used to filter constitution XLSX files so only use in-force and build metadata_dict
- metadata_list.xml: From constituteproject.org. Not used because metadata are obtained from const_list
- revised_ontology.csv: Revised ontology data used to generate topic data model files

Model:
    Dictionaries:

    - topics_dict: key is a topic key, value is dictionary containing labels path, description, and keywords
    - documents_dict: key is a constitution ID (used to prefix segment IDs), value is a document name, and metadata
    - segments_dict: key is a segment ID (<doc_id>/<sentence_number>), value is sentence text

    Lists:

    - encoded_segments: List of IDs of encoded segments
    - segment_encodings: List of encoding vectors for encoded segments in same order so can use index.
    - encoded_topics: List of IDs of encoded topics (all of them)
    - topic_encodings: List of encoding vectors for encoded topics in same order so can use index.
  
    Matrices:

    - topic_segment_matrix: Similarity matrix with topics in rows and segments in columns

Dependencies:

- USE-4 (or some other encoder)


"""

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import process_topics
import process_documents
import process_segments


from packages import *
from nlp import *

def main():

    model_path = './model/'

    encoder_path = '../../_external_models/'
    # Load an encoder
    encoder = hub.load(encoder_path + 'use-4')

    # Process topics *********************************************************************
    print('Processing topics…')
    # This is the topic tree from the Constitute Project site
    data_path = 'data/'

    topics_dict,topic_encodings,encoded_topics = process_topics.process(data_path,encoder)
    model_filename = model_path + 'topics_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(topics_dict, f)
        f.close()
    model_filename = model_path + 'topic_encodings.json'
    with open(model_filename, 'w') as f:
        json.dump(topic_encodings, f)
        f.close()
    model_filename = model_path + 'encoded_topics.json'
    with open(model_filename, 'w') as f:
        json.dump(encoded_topics, f)
        f.close()
    print('Finished processing and serialising topics:', len(topics_dict), len(encoded_topics))

    # Process documents *****************************************************************
    print('Processing documents…')
    documents_dict = process_documents.process(data_path)
    model_filename = model_path + 'documents_dict.json'
    with open(model_filename, 'w') as outfile:
        json.dump(documents_dict, outfile)
        outfile.close() 
    print('Finished processing and serialising documents:', len(documents_dict))
    
    # Process segments ******************************************************************
    print('Processing segments…')
    segments_dict,segment_encodings,encoded_segments = process_segments.process(documents_dict,data_path,encoder)
    model_filename = model_path + 'segments_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(segments_dict, f)
        f.close()
    model_filename = model_path + 'segment_encodings.json'
    with open(model_filename, 'w') as f:
        json.dump(segment_encodings, f)
        f.close()
    model_filename = model_path + 'encoded_segments.json'
    with open(model_filename, 'w') as f:
        json.dump(encoded_segments, f)
        f.close()
    print('Finished processing and serialising segments:', len(segments_dict))

    # Building topic_segment similarity matrix ********************************************************
    print('Building topics-segments similarity matrix…')
    start_time = time.time()
    sim_matrix = cdist(topic_encodings, segment_encodings,ad.angular_distance)
    sim_matrix = np.array(sim_matrix).tolist()
    model_filename = model_path + 'topic_segment_matrix.json'
    with open(model_filename, 'w') as outfile:
        json.dump(sim_matrix, outfile)
        outfile.close() 
    print(time.time() - start_time)
    print('Finished building and serialising topics-segments similarity matrix')
 
if __name__ == '__main__':
    main()
