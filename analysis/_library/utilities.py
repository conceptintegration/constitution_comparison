#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023-2025, Roy and Sally Gardner'

from packages import *

twenty_distinct_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0',\
                        '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324',\
                        '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff',\
                        '#000000', '#fffac8']


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





