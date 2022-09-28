import pdfplumber
import re
from scripts.preparation import clean_list_of_text


def extract_tables(path):
    doc = pdfplumber.open(path)
    pages = doc.pages
    tables_dict = {}
    tables_list = []
    
    for i in enumerate(pages):
        j = i[0]
        page = pages[j]
        tables_list.append(page.find_tables(
            table_settings = {
                'vertical_strategy': 'lines',
                'horizontal_strategy': 'lines'
            }))
        tables_dict[j] = tables_list[j]
        
    clean_tables_dict = {k:v for k, v in tables_dict.items() if v}
    
    if not any(clean_tables_dict):
        clean_tables_dict = None
    else:
        clean_tables_dict
        
    return clean_tables_dict


def split_in_sentences(lst):
    """
    Take the cleaned list returned by clean_text and split the text in sentences.
    You now have the cleaned text in a nested list.
    The first level of the list is the page of the document, the second level is the sentence.
    """
    
    clean_sent = []
    for text in lst:
        text = re.split('[.?]', text)
        clean_sent.append(text)
    return clean_sent


def get_index_of_words(pages, words=None):
    """
    Checks pages for occurences of a list of words.
    The default list of words consists of variations of 'Inventarislijst'.
    """
    
    if words is None:
        words = ['Inventarisatielijst', 'inventarisatielijst',
                 'Inventarislijst', 'inventarislijst',
                 'Inventarisatie', 'inventarisatie']
    page_indexes = []
    for page in pages:
        for sentence in page:
            if any(word in sentence for word in words):
                page_index = pages.index(page)
                page_indexes.append(page_index)

    return(page_indexes)


def get_table_pages(path, text):
    """
    Takes path to a pdf file and predicts the page on which the table or 'Inventarislijst' can be found.
    Applys logical rules to the found pages. These rules are based on assumptions.
    """

    tables = extract_tables(path)
    sentences = split_in_sentences(clean_list_of_text(text))    
    
    pages_with_words = get_index_of_words(sentences)
    
    try:
        table_indexes = list(tables.keys())
    except:
        table_indexes = []
    
    indexes_with_tables_and_words = [i for i in table_indexes if i in pages_with_words]
    
    predicted_pages = []
    num_of_pages = len(sentences)
    num_of_tables = len(table_indexes)
    
    if num_of_tables > 0:
        final_table_index = max(table_indexes)
        final_table_page = max(table_indexes) + 1
    else:
        final_table_index = None
        final_table_page = None
    
    # If we find no tables, return None 
    if num_of_tables == 0:
        # print('I found no table at all. Nada!')
        return None
      
    # If we find only one table, the predicted index is equal to that of the table
    if num_of_tables == 1:
        # print('I found exactly 1 table!')
        predicted_index = table_indexes[0]
        predicted_pages.append(predicted_index)
        
    if num_of_tables == num_of_pages:
        # print('I found only tables in this doc')
        return None
    
    # If we find a table on the final page, the predicted index is equal to the final index
    if num_of_tables > 1 and final_table_page == num_of_pages:
        # print('I found a table on the final page...')
        predicted_index = final_table_index
        predicted_pages.append(predicted_index)
    
    # Check if the pages before the final page are also tables   
        i = 1
        j = 2 
        while (table_indexes[-i] - table_indexes[-j] == 1):
            # print('...and on the page before that one')
            predicted_index = table_indexes[-j]
            predicted_pages.append(predicted_index)
            i += 1
            j += 1
            if i == num_of_tables:
                break
            
    # If there is table found on an index containing words like 'Inventarislijst', the predicted index is equal 
    elif num_of_tables > 1 and len(indexes_with_tables_and_words) == 1:
        # print('I found a table on a page mentioning an Inventarisatielijst of some sort')
        predicted_index = indexes_with_tables_and_words[0]
        predicted_pages.append(predicted_index)
    
    # If there are more duplicate pages, we pick the max, becaused the table is expected to be more at the end
    elif len(indexes_with_tables_and_words) > 1:
        # print('I found a table on a page mentioning an Inventarisatielijst multiple times')
        predicted_index = max(indexes_with_tables_and_words)
        predicted_pages.append(predicted_index)
    
    else:
        return None
    
    # Add 1 to go from index to page
    predicted_pages = [x + 1 for x in predicted_pages]
    # Sort ascending
    predicted_pages.sort()
    
    return predicted_pages

def get_table_pages_no_rules(path, text):
    """
    Takes path to a pdf file and predicts the page on which the table or 'Inventarislijst' can be found.
    Applies no logical rules to the found pages.
    """

    tables = extract_tables(path)
    sentences = split_in_sentences(clean_list_of_text(text))    
    
    pages_with_words = get_index_of_words(sentences)
    
    try:
        table_indexes = list(tables.keys())
    except:
        table_indexes = []
    
    indexes_with_tables_and_words = [i for i in table_indexes if i in pages_with_words]
    
    predicted_pages = indexes_with_tables_and_words
    
    # Add 1 to go from index to page
    predicted_pages = [x + 1 for x in predicted_pages]
    # Sort ascending
    predicted_pages.sort()
    
    return predicted_pages
