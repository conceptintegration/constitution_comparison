#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'

"""

Generates following model files from constitution XML:

- documents_dict.json
- segments_dict.json
- segment_encodings.json
- encoded_segments.json
- segments_matrix.json

This process DOES NOT segment constitution sections.

"""

from packages import *
from utilities import *

def process(config):

    have_metadata = False
    metadata_dict = {}

    data_path,model_path,encoder_path = validate_paths(config['shared'])
    metadata_file = data_path + config['constitutions']['metadata_file']


    if len(config['constitutions']['metadata_file']) == 0:
        have_metadata = False
    elif len(config['constitutions']['metadata_file']) > 0 and not os.path.exists(metadata_file):
        raise PathException(f"Could not locate the metadata file {metadata_file}")
    else:
        have_metadata = True

    encoder = hub.load(encoder_path)

    # Key is a segment identifier, value is a text segment
    documents_dict = {}
    segments_dict = {}

    # Read metadata
    if have_metadata:
        with open(metadata_file, encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            # Get the header row
            header = next(reader)
            # Put the data into dictionary
            metadata_dict = {row[0]:row[1:] for row in reader if len(row[0])>0}
            
    const_path = data_path + config['constitutions']['constitutions_path']
    _, _, files = next(os.walk(const_path))
    files = [f for f in files if not f[0] == '.']

    print('Segmenting…')
    for i, file in enumerate(files):
        constitution_id = os.path.splitext(file)[0]
        documents_dict[constitution_id] = {}
        documents_dict[constitution_id]['name'] = constitution_id

        if have_metadata and constitution_id in metadata_dict:
            metadata = metadata_dict[constitution_id]
            for metadata_index,field_name in enumerate(header[1:]):
                documents_dict[constitution_id][field_name] = metadata[metadata_index]

        xml_file = const_path + file
        tree = etree.parse(xml_file)
        results = []
        for type_ in config['constitutions']['element_types']:
            search_str = ".//*[@type='" + type_ + "']"
            results.extend(tree.findall(search_str))

        for elem in results:
            # Get the section ID which we are calling the segment_id because of data model conventions
            segment_id = constitution_id + '/' + elem.get('uri').split('/')[1]

            # Content contains the text
            content = elem.findall('content')
            if len(content) > 0:
                for content_elem in content:
                    if 'en' in content_elem.values():
                        text = content_elem.text
                        if text == None:
                            continue
                        if not type(text) == str:
                            continue
                        else:
                            text = html.unescape(text)
                        if len(text.strip()) == 0:
                            continue
                        
                        segments_dict[segment_id] = {}
                        segments_dict[segment_id]['text'] = text.strip()

    segment_encodings,encoded_segments = encode_segments(segments_dict,encoder,split_size=20)
    segments_matrix = build_segment_segments_matrix(segment_encodings,model_path)
 
    print('Serialising model files…')
    model_filename = model_path + 'documents_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(documents_dict, f)
    model_filename = model_path + 'segments_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(segments_dict, f)
    model_filename = model_path + 'encoded_segments.json'
    with open(model_filename, 'w') as f:
        json.dump(encoded_segments, f)
    model_filename = model_path + 'segment_encodings.json'
    with open(model_filename, 'w') as f:
        json.dump(segment_encodings, f)
    model_filename = model_path + 'segments_matrix.json'
    with open(model_filename, 'w') as f:
        json.dump(np.array(segments_matrix).tolist(), f)

    print('Finished processing.\n')

    return segment_encodings
