#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2024, Roy and Sally Gardner'

from packages import *

def get_max_scores(matrix):
    """
    Collect the maximum similarity scores from a matrix.
    The first pass collects the row and column indices of the maximum value in a row
    The second pass transposes the matrix to find the maximum values for original matrix columns (rows in the transposed matrix) not captured in the first pass.
    The rationale is that a row segment A may be maximally similar to a column segment B but B might not be maximally similar to A
    return: A list of maximum score values
    """
    row_indices = [(i,np.argmax(row)) for i,row in enumerate(matrix)]
    # Now transpose because the max of a row might not be the max of the column containing the row's max
    matrix_transpose = matrix.T
    # Reverse the indices because the row max is now a column max in the original matrix
    row_indices.extend([(np.argmax(row),i) for i,row in enumerate(matrix_transpose)])
    row_indices = set(row_indices)
    scores = [matrix[indices[0]][indices[1]] for indices in row_indices]
    return scores

