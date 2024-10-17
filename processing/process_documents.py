#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'


"""

"""

from packages import *

def process(data_path):

    # Dictionary to connect doc IDs (the key) to doc titles (the value)
    documents_dict = {}

    # Use only in force constitutions from the site
    with open(data_path + 'const_list.json', 'r') as f:
        const_list = json.load(f)
        f.close() 

    # Build dictionary of in-force constitutions
    const_dict = {d['id']:d for d in const_list}

    xml_dir = data_path + 'constitutions_xml/'
    _, _, files = next(os.walk(xml_dir))
    files = [f for f in files if not f[0] == '.']
    for i, file in enumerate(files):
        constitution_id = os.path.splitext(file)[0]
        if constitution_id not in const_dict:
            continue
        documents_dict[constitution_id] = {}
        documents_dict[constitution_id]['name'] = constitution_id
        documents_dict[constitution_id]['region'] = const_dict[constitution_id]['region']
        documents_dict[constitution_id]['year_enacted'] = const_dict[constitution_id]['year_enacted']

    return documents_dict
 


