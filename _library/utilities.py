#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy and Sally Gardner'

from packages import *

def do_load(model_path,exclusion_list=[],verbose=True):
    if verbose:
        print('Loading model…')
    model_dict = {}

    _, _, files = next(os.walk(model_path))
    files = [f for f in files if f.endswith('.json') and not f in exclusion_list]
    for file in files:
        model_name = os.path.splitext(file)[0]
        with open(model_path + file, 'r', encoding='utf-8') as f:
            model_dict[model_name] = json.load(f)
            f.close() 
    if verbose:
        print('Finished loading model.')
    return model_dict

def popup(text):
    display(Javascript("alert('{}')".format(text)))

def alert(msg):
    from IPython.display import Javascript

    def popup(text):
        display(Javascript("alert('{}')".format(text)))
    popup(msg)

def encode_text(text_list, encoder):
    """
    Get a list of encoding vectors for the text segments in text_list
    param text_list: A list of strings containing text to be encoded
    param encoder: The encoder, e.g. USE v4
    return A list of encoding vectors in the same order as text_list
    """
    encodings = encoder(text_list)
    return np.array(encodings).tolist()




