#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2021, Roy Gardner'

import json

def main():
    # Load model
    
    path_to_model = './model/'

    print('Deserialising model…')

    with open(path_to_model + 'document_dict.json', 'r') as f:
        document_dict = json.load(f)
        f.close() 
    with open(path_to_model + 'sentence_dict.json', 'r') as f:
        sentence_dict = json.load(f)
        f.close() 
    with open(path_to_model + 'sentence_encodings.json', 'r') as f:
        sentence_encodings = json.load(f)
        f.close() 
    with open(path_to_model + 'encoded_sentences.json', 'r') as f:
        encoded_sentences = json.load(f)
        f.close() 
    with open(path_to_model + 'topic_dict.json', 'r') as f:
        topic_dict = json.load(f)
        f.close() 
    with open(path_to_model + 'encoded_topics.json', 'r') as f:
        encoded_topics = json.load(f)
        f.close() 
    with open(path_to_model + 'topic_encodings.json', 'r') as f:
        topic_encodings = json.load(f)
        f.close()   
    with open(path_to_model + 'similarity_matrix.json', 'r') as f:
        similarity_matrix = json.load(f)
        f.close()   

    print('Number of documents:',len(document_dict))
    print('Number of sentences:',len(sentence_dict))
    print('Number of topics:',len(topic_dict))
    print('')

    print('Number of encoded sentences:',len(sentence_encodings))
    assert(len(sentence_encodings) == len(encoded_sentences))
    print('Number of encoded topics:',len(topic_encodings))
    assert(len(topic_encodings) == len(encoded_topics))
    print('')

    print('Sim matrix rows:',len(similarity_matrix))
    assert(len(similarity_matrix) == len(encoded_topics))
    print('Sim matrix columns:',len(similarity_matrix[0]))
    assert(len(similarity_matrix[0]) == len(encoded_sentences))
    print('')

if __name__ == '__main__':
    main()
