#!/bin/python
# -*- coding: utf-8 -*-

from packages import *

class PathException(Exception):
  pass

def validate_paths(config):
    data_path = config['data_path']
    model_path = config['model_path']
    encoder_path = config['encoder_path']

    # Check paths
    if not data_path.endswith(os.sep):
        data_path = data_path + os.sep
    if not os.path.exists(data_path):
        raise PathException('Data path cannot be found please check the configuration.\n')
    
    # Create the model path if it doesn't already exist
    if not model_path.endswith(os.sep):
        model_path = model_path + os.sep
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    if not encoder_path.endswith(os.sep):
        encoder_path = encoder_path + os.sep
    if not os.path.exists(encoder_path):
        raise PathException('Encoder cannot be found please check the configuration.\n')
    
    return data_path,model_path,encoder_path

class DataFieldException(Exception):
  pass

def encode_topics(topics_dict,encoder,split_size=10):
    # Encode
    print('Encoding topics…')
    encoded_topics = list(topics_dict.keys())
    topics_text_list = [v['encoded_text'] for _,v in topics_dict.items()]
    # Split the list so the encoder doesn't have to work too hard
    split_list = np.array_split(topics_text_list,split_size)

    topic_encodings = []
    for i,l in enumerate(split_list):
        split = list(l)
        encodings = encoder(split)
        assert(len(encodings) == len(split))
        topic_encodings.extend(np.array(encodings).tolist())

    return topic_encodings,encoded_topics

def encode_segments(segments_dict,encoder,split_size=80):
    # Encode
    print('Encoding segments…')
    encoded_segments = list(segments_dict.keys())
    segments_text_list = [v['text'] for _,v in segments_dict.items()]
    # Split the list so the encoder doesn't have to work too hard
    split_list = np.array_split(segments_text_list,split_size)

    segment_encodings = []
    for i,l in enumerate(split_list):
        split = list(l)
        encodings = encoder(split)
        assert(len(encodings) == len(split))
        segment_encodings.extend(np.array(encodings).tolist())

    return segment_encodings,encoded_segments

def build_topic_segments_matrix(topic_encodings,segment_encodings):
    print('Building topic-segment matrix…')
    matrix = cdist(topic_encodings,segment_encodings,ad.angular_distance)
    return matrix

def build_segment_segments_matrix(segment_encodings,model_path):
    print('Building segment-segment matrix…')
    # This has to be a full matrix as it's being used to build sub-matrices for KDE-PDF operations
    matrix = cdist(segment_encodings,segment_encodings,ad.angular_distance)
    return matrix
