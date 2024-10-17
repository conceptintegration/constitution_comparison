#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023, Roy Gardner'



from packages import *
from nlp import *

def get_min_header():
    """
    The constitution xlsx files are headerless so define the minimun column set
    return: List of column headers
    """
    header_min = []
    header_min.append('row')
    header_min.append('parent')
    header_min.append('header_en')
    header_min.append('header_ar')
    header_min.append('header_es')
    header_min.append('structure')
    header_min.append('row_type')
    header_min.append('text_en')
    header_min.append('text_ar')
    header_min.append('text_es')
    return header_min

def xlsx_to_rows_list(xlsx_file):
    """
    Convert XLSX file into a list of dictionaries with one dictionary per row.
    Dictionary keys are auto generated column names provided by header_min
    param xlsx_file: XLSX file with path
    return List of dicts where each dict is an XLSX row
    """
    header_min = get_min_header()
    # This is the name of our CSV
    name = os.path.splitext(os.path.basename(xlsx_file))[0]
    name = '_'.join(name.split())
    # Read the XLSX into a dataframe. Using sheet_name = 0
    data_xls = pd.read_excel(xlsx_file, 0, index_col=None, header=None)
    # Number of columns is file dependent
    num_columns = len(data_xls.columns)
    # Make sure our header is the correct length for the file
    header = []
    header.extend(header_min)
    i = 1
    while len(header) < num_columns:
        header.append('topic_' + str(i))
        i += 1
    # Update the header
    data_xls.columns = header
    # Deal with nan values by substituting -1
    data_xls = data_xls.fillna(int(-1))
    dict_list = data_xls.to_dict('records')
    return dict_list

def main():

    model_path = './model/'
    data_path = './data/'

    xml_dir = data_path + 'constitutions_xml/'
    _, _, files = next(os.walk(xml_dir))
    xml_files = [f for f in files if not f[0] == '.']

    xlsx_dir = data_path + 'constitutions_xlsx/'
    _, _, files = next(os.walk(xlsx_dir))
    xlsx_files = [f for f in files if not f[0] == '.']

    # Find the XML files that have a corresponding XLSX file
    xml_ids = [os.path.splitext(file)[0] for file in xml_files]
    xlsx_ids = [os.path.splitext(file)[0] for file in xlsx_files]

    process_ids = [id_ for id_ in xml_ids if id_ in xlsx_ids]
    print(len(process_ids))

    count_dict = {}

    for i, file_id in enumerate(process_ids):
        count_dict[file_id] = [0,0]

        sys.stdout.write("\r" + str(i))
        sys.stdout.flush()

        xml_file = xml_dir + file_id + '.xml'
        xlsx_file = xlsx_dir + file_id + '.xlsx'

        tree = etree.parse(xml_file)

        segment_count = 0
        for elem in tree.findall(".//*[@type='body']") + tree.findall(".//*[@type='list']"):
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
                        segment_count += 1
        #print(file_id,segment_count)
        count_dict[file_id][0] = segment_count

        segment_count = 0
        rows_list = xlsx_to_rows_list(xlsx_file)    
        for _, row_dict in enumerate(rows_list):
            if row_dict['row'] == -1 or row_dict['row_type'] == -1:
                continue
            if row_dict['row_type'] != 'body':
                continue
            # Build the segments dictionary
            text = row_dict['text_en']
            if type(text) != str:
                continue
            segment_count += 1
        count_dict[file_id][1] = segment_count

    sys.stdout.write("\r")
    sys.stdout.flush()
    header = []
    header.append('Constitution')
    header.append('# XML sections')
    header.append('# XLSX sections')
    header.append('Difference (XML - XLSX)')

    csv_row_list = []
    csv_row_list.append(header)
    
    for k,v in count_dict.items():
        csv_row = []        
        csv_row.append(k)
        csv_row.append(v[0])
        csv_row.append(v[1])
        csv_row.append(v[0] - v[1])
        csv_row_list.append(csv_row)
           
    file_name = './xml_versus_xlsx.csv'
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_row_list)
    f.close()



if __name__ == '__main__':
    main()
