#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2024, Roy Gardner'


"""

"""

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from packages import *

def main():
    print('Loading model files…')

    model_path = './model/'
    with open(model_path + 'segment_encodings.json', 'r') as f:
        segment_encodings = json.load(f)
        f.close() 
    print('Finished loading model files.')



    # Building segments similarity matrix ********************************************************
    print('Building segments similarity matrix…')

    #n = len(segment_encodings)
    #matrix = np.zeros((n, n))
    #row,col = np.triu_indices(n,1)
    #matrix[row,col] = pdist(segment_encodings,ad.angular_distance)

    # This has to be a full matrix if it's being used to build sub-matrices for KDE-PDF operations
    matrix = cdist(segment_encodings,segment_encodings,ad.angular_distance)

    print('Serialising matrix…')
    filename = model_path + 'segments_matrix.json'
    with open(filename, 'w') as f:
        json.dump(np.array(matrix).tolist(), f)
        f.close()

    matrices_map = {}
    matrices_map['matrix_list'] = []
    matrix_dict = {}
    matrix_dict['name'] = 'CCP Chile drafts and current'
    matrix_dict['description'] = 'Analysis of CCP Chile draft and current constitutions'
    matrix_dict['matrix'] = 'segments_matrix'
    matrix_dict['indices'] = ''
    matrices_map['matrix_list'].append(matrix_dict)
    
    filename = model_path + 'matrices_map.json'
    with open(filename, 'w') as f:
        json.dump(matrices_map, f)
        f.close()


    print('Finished building and serialising segments similarity matrix')



if __name__ == '__main__':
    main()
