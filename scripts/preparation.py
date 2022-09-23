from nltk.corpus import stopwords
import pdfplumber
import spacy
import re


def extract_text(file_name, threshold=0.03):
    """
    Calculates the percentage of document that is covered by (searchable) text.
    If the returned percentage of text is very low, the document is most likely a scanned PDF.
    Extracts the text of the documents above a given threshold. The default threshold is 3%.

    """
    total_page_area = 0.0
    total_text_area = 0.0
    text = []
    
    try:
        doc = pdfplumber.open(file_name)
        pages = doc.pages
        num_pages = len(doc.pages)

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
            for page in pages:
                text.append(page.extract_text())
        else:
            text = None

        doc.close()
        return text
        
    except Exception as e:
        print(f"The following exception: {e}, occured at {file_name}")
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
    Simple lemmatizer using spaC and dutch stopword list.
    """
    doc = nlp(text)
    lemmas = [t.lemma_ for t in doc if t.lemma_ not in stopwords]
    
    return lemmas


def preprocess(df, threshold):
    """
    Apply preprocessing functions.
    """

    df['text'] = df['path'].apply(lambda x: extract_text(x, threshold))
    df['clean_text'] = df['text'].apply(lambda x: clean_list_of_text(x))

    return df
