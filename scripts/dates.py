import re
import spacy
import locale
from itertools import *
from re import compile, match
from collections import Counter
from datetime import datetime, timedelta


def extract_dates_from_text(text, nlp):
    """
    Extracts the entities of type DATE from the text and perform basic filtering.
    Returns a list containing datetime objects.
    """
    
    flat_text = ' '.join(map(str, text))  # flatten the list input to a string
    doc = nlp(flat_text)
    
    # get the entities grouped by DATE type and create a list of strings
    entities = {key: list(g) for key, g in groupby(sorted(doc.ents, key=lambda x: x.label_), lambda x: x.label_)}
    try:
        dates_in_strings = [i.text for i in entities['DATE']]    
    except KeyError:
        dates_in_strings = ['31 december 2999']  # default value if no dates are found in the doc
        
    # extract the dates following the correct pattern: "## month YYYY" (where # is a digit)
    regexp = compile(r'^\d{1,2} [a-zA-Z]+ \d{4}$')
    cleaned_dates_in_strings = [line for line in dates_in_strings if regexp.match(line)]
    
    # transform the list of strings to a list of date time objects
    locale.setlocale(locale.LC_ALL, 'nl_NL.utf-8')    
    date_time_obj_list = []
    
    for date in cleaned_dates_in_strings:
        try:
            date_time_obj_list.append(datetime.strptime(date, '%d %B %Y'))
        except ValueError:
            pass

    return date_time_obj_list


def get_dates(text, nlp):
    """
    Predicts the dates from the datetime object lists using logic.
    Transforms the dates to the following format: 19-8-2021.
    """

    date_time_obj_list = extract_dates_from_text(text, nlp)
            
    # Predicts the Decision Date based on occurrence
    try:
        decision_date = date_time_obj_list[0]
        converted_decision_date = decision_date.strftime('%-d-%-m-%Y')
        if converted_decision_date[0] == '0':
            converted_decision_date = converted_decision_date[1:]
        else:
            converted_decision_date
    except IndexError:
        converted_decision_date = None
    
    # Predicts the Request Date based on occurrence
    try:
        request_date = date_time_obj_list[1]
        converted_request_date = request_date.strftime('%-d-%-m-%Y')
        if converted_request_date[0] == '0':
            converted_request_date = converted_request_date[1:]
        else:
            converted_request_date
    except IndexError:
        converted_request_date = None
        
    return converted_decision_date, converted_request_date
