#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'

#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'

"""

"""

from packages import *

def process(documents_dict,data_path,encoder):
    error_list = []
    # Key is a segment identifier, value is a text segment
    segments_dict = {}

    xml_dir = data_path + 'constitutions_xml/'
    _, _, files = next(os.walk(xml_dir))
    files = [f for f in files if not f[0] == '.']
    for i, file in enumerate(files):
        sys.stdout.write("\r" + str(i))
        sys.stdout.flush()

        constitution_id = os.path.splitext(file)[0]
        if constitution_id not in documents_dict:
            continue

        xml_file = xml_dir + file
        tree = etree.parse(xml_file)
        for elem in tree.findall(".//*[@type='body']") + tree.findall(".//*[@type='list']"):
            # Content contains the text
            content = elem.findall('content')
            if len(content) > 0:
                for content_elem in content:
                    if 'en' in content_elem.values():
                        text = content_elem.text
                        if text == None:
                            text = ''
                            error_list.append((constitution_id,elem.get('uri').split('/')[1],'None'))
                        if not type(text) == str:
                            text == ''
                            error_list.append((constitution_id,elem.get('uri').split('/')[1],'Not a string'))
                        else:
                            text = html.unescape(text)
                        segment_id = constitution_id + '/' + elem.get('uri').split('/')[1]
                        segments_dict[segment_id] = {}
                        segments_dict[segment_id]['text'] = text.strip()
                    
    sys.stdout.write("\r")
    sys.stdout.flush()

    encoded_segments = []
    segments_text_list = []
    for k,v in segments_dict.items():
        if v['text'] == None:
            continue
        if len(v['text']) > 0:
            segments_text_list.append(v['text'])
            encoded_segments.append(k)

    print('Encoding:',len(segments_text_list))

    indices = list(range(0,len(segments_text_list)))
    split_list = np.array_split(indices,100)
    print('Split list')
    segment_encodings = []
    print('Starting split loop…')
    for i,l in enumerate(split_list):
        #print('Encoding',str(i + 1),'of 100')
        split = [segments_text_list[index] for index in list(l)]
        encodings = encoder(split)
        assert(len(encodings) == len(split))
        segment_encodings.extend(np.array(encodings).tolist())
    print('Finished split loop')
 
    # Write errrors to disk
    model_filename = './error_list.json'
    with open(model_filename, 'w') as outfile:
        json.dump(error_list, outfile)
        outfile.close() 
        
    return segments_dict,segment_encodings,encoded_segments

