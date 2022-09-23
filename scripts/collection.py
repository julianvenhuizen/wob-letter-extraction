import os
import re
import pandas as pd
import tkinter.filedialog as tkfd


def generate_index(path=None, max_records=0):
    """
    Generates an index of documents in a given directory.
    """
    path = path if path else tkfd.askdirectory()    
    data = pd.DataFrame(columns=['file_name', 'folder', 'path'])
    
    for root, dir, files in os.walk(path):
        names = [f for f in files if not f.startswith('~')]
        paths = [os.path.join(root, f) for f in files]
        grand_parent = [os.path.dirname(os.path.dirname(p)) for p in paths]
        df = pd.DataFrame({'file_name': names, 'folder': grand_parent, 'path': paths})
        if max_records and (Data.shape[0] > max_records):
            break

        data = pd.concat([data, df], ignore_index=True)
        
    return data


def filter_and_clean_index(df):
    """
    Cleans the index by filtering files.
    """
    df['folder'] = [re.sub(r'(.*)/', '', str(x)) for x in df['folder']] # get the main folder name
    df = df[df['file_name'] != '.DS_Store'] # remove the .DS_Store files from the dataframe
    df = df[df['file_name'].str.contains('|'.join(['bijlage', 'bijlagen']), case=False)==False] # remove the bijlagen
    df = df.reset_index(drop=True)
    
    return df
