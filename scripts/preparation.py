from nltk.corpus import stopwords
import pandas as pd
import pdfplumber
import spacy
import re


def open_pdf(file_name, threshold=0.03):
    total_page_area = 0.0
    total_text_area = 0.0
    text = []
    tables_list = []
    tables_dict = {}

    try:
        doc = pdfplumber.open(file_name)
        pages = doc.pages

        for page_number, page in enumerate(pages):
            total_page_area = total_page_area + abs(page.width * page.height)
            text_area = 0.0
            i = 0
            for i in range(len(page.chars)):
                text_area = text_area + abs(page.chars[i]['width'] * page.chars[i]['height'])
            total_text_area = total_text_area + text_area
            i += 1

        percentage = total_text_area / total_page_area
        if percentage >= threshold:
            for i in enumerate(pages):
                j = i[0]
                page = pages[j]
                text.append(page.extract_text())
                tables_list.append(page.find_tables(
                    table_settings={
                        'vertical_strategy': 'lines',
                        'horizontal_strategy': 'lines'
                    }
                ))
                tables_dict[j] = tables_list[j]
        else:
            text = None
            tables_dict = None

        doc.close()

        tables = {k: v for k, v in tables_dict.items() if v}
        if not any(tables):
            tables = None
        return text, tables

    except Exception as e:
        print(f"The following exception: {e}, occurred at {file_name}")
        return None


def open_pdf_no_classifier(file_name):
    text = []
    tables_list = []
    tables_dict = {}

    try:
        doc = pdfplumber.open(file_name)
        pages = doc.pages

        for i in enumerate(pages):
            j = i[0]
            page = pages[j]
            text.append(page.extract_text())
            tables_list.append(page.find_tables(
                table_settings={
                    'vertical_strategy': 'lines',
                    'horizontal_strategy': 'lines'
                }
            ))
            tables_dict[j] = tables_list[j]
        doc.close()
        tables = {k: v for k, v in tables_dict.items() if v}
        if not any(tables):
            tables = None
        return text, tables
    except Exception as e:
        print(f"The following exception: {e}, occurred at {file_name}")
        return None


def clean_text(text):
    """
    Performs basic cleaning operations.
    """
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r" +", " ", text)
    text = text.replace("'", "")
    text = text.strip()
    
    return text


def clean_list_of_text(list_of_text):
    """
    Takes the list of text returned by get_text_and_words_and_tables and cleans it using regex.
    """
    
    clean_list = []
    try:
        for text in list_of_text:
            text = re.sub(r"\\n", " ", text)
            text = re.sub(r"\n", " ", text)
            text = re.sub(r" +", " ", text)
            text = text.strip()
            clean_list.append(text)
    except:
        clean_list = []

    return clean_list


def split_in_sentences(text):
    """
    Splits the text in sentences, delimited by a period or question mark.
    """

    text = re.split('[.?]', text)
    sentences = []
    for sent in text:
        sentences.append(sent)
        
    return sentences


def lemmatizer(text, nlp, stopwords):
    """
    Simple lemmatizer using spaCy and NLTK's Dutch stopword list.
    """
    lemmas = []

    try:
        doc = nlp(text)
        lemmas = [t.lemma_ for t in doc if t.lemma_ not in stopwords]
    except:
        pass

    return lemmas


def preprocess(df, classifier=True, threshold=0.03):
    """
    Apply preprocessing functions.
    """
    # df['text'] = df['path'].apply(lambda x: extract_text(x, threshold))
    if classifier is True:
        df['text'], df['tables'] = zip(*df['path'].apply(lambda x: open_pdf(x, threshold)))
    else:
        df['text'], df['tables'] = zip(*df['path'].apply(lambda x: open_pdf_no_classifier(x)))

    df['clean_text'] = df['text'].apply(lambda x: clean_list_of_text(x))

    return df
