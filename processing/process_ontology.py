#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'


"""

Generates following model files from the CCP ontology:

- topics_dict.json
- topic_encodings.json
- encoded_topics.json

Encoded topic text comprises the concatenated topic label and topic description.

"""

from packages import *
from utilities import *

def process(config):

    data_path,model_path,encoder_path = validate_paths(config['shared'])
    ont_path = data_path + config['ontology']['ontology_file']
    if not os.path.exists(ont_path):
        raise PathException(f"Could not locate the ontology file {config['ontology']['ontology_file']}")
    
    encoder = hub.load(encoder_path)

    ontology_config = config['ontology']

    topics_dict = {}

    # Read the ontology
    with open(ont_path, encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        # Get the header row
        header = next(reader)
        # Put the remaining rows into a list of lists
        data = [row for row in reader if len(row[0])>0]

    # Create a dictionary before distributing into a CSV
    for row in data:
        # Every row is terminal
        topic_id = row[header.index(ontology_config['key_field'])]
        label = row[header.index(ontology_config['label_field'])]
        desc = row[header.index(ontology_config['description_field'])]

        topics_dict[topic_id] = {}
        topics_dict[topic_id]['label'] = label
        topics_dict[topic_id]['description'] = desc    
        topics_dict[topic_id]['encoded_text'] = label + '. ' + desc
       

    topics_encodings,encoded_topics = encode_topics(topics_dict,encoder,split_size=10)

    print('Serialising model files…')
    model_filename = model_path + 'topics_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(topics_dict, f)
    model_filename = model_path + 'encoded_topics.json'
    with open(model_filename, 'w') as f:
        json.dump(encoded_topics, f)
    model_filename = model_path + 'topics_encodings.json'
    with open(model_filename, 'w') as f:
        json.dump(topics_encodings, f)

    print('Finished processing\n')

    return topics_encodings
