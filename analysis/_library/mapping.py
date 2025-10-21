#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2024-2025, Roy Gardner and Sally Gardner'

from packages import *

def compute_marginal_top_k(matrix,k=5):
    """
    Keep only top k topics per segment.
    
    matrix: (topics × segments)
    """
    n_topics, n_segments = matrix.shape
    filtered = np.zeros_like(matrix)
    
    for seg_idx in range(n_segments):
        segment_scores = matrix[:,seg_idx]
        # Get indices of top k values
        top_k_indices = np.argpartition(segment_scores,-k)[-k:]
        filtered[top_k_indices,seg_idx] = segment_scores[top_k_indices]
    
    # Compute marginal (weighted by actual scores)
    marginal = filtered.sum(axis=1) / n_segments
    
    return marginal


def analyse_topic_alignment(m1,m2,k=10):
    """
    Compute topic alignment using top k filtering.
    """
    # Filter to top k topics per segment
    marginal_A = compute_marginal_top_k(m1,k=k)
    marginal_B = compute_marginal_top_k(m2,k=k)
    
    # Remove topics with zero coverage in both
    mask = (marginal_A > 0) | (marginal_B > 0)
    
    #print(f"Active topics: {mask.sum()} / {len(mask)}")
    #print(f"Marginal A: min={marginal_A[mask].min():.4f},\
    #        max={marginal_A[mask].max():.4f}, std={marginal_A[mask].std():.4f}")
    #print(f"Marginal B: min={marginal_B[mask].min():.4f},\
    #        max={marginal_B[mask].max():.4f}, std={marginal_B[mask].std():.4f}")
    
    # Compute similarity
    correlation, p = stats.pearsonr(marginal_A[mask], marginal_B[mask])
    cosine = cosine_similarity([marginal_A[mask]], [marginal_B[mask]])[0, 0]
    
    return {
        'correlation': correlation,
        'cosine': cosine,
        'p_value': p,
        'active_topics': mask.sum(),
        'marginal_A': marginal_A,
        'marginal_B': marginal_B
    }



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

