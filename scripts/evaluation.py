import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

import seaborn as sns
import matplotlib.pyplot as plt

from preprocessing import lemmatizer


def is_equal(a, b):
    return a == b


def jaccard_similarity(doc1, doc2):
    if type(doc1) == list:
        [x.lower() for x in doc1]
        words_doc1 = set(doc1)
    else:
        words_doc1 = set(doc1.lower().split())
    if type(doc2) == list:
        [x.lower() for x in doc2]
        words_doc2 = set(doc2)
    else:
        words_doc2 = set(doc2.lower().split())
    
    # Find the intersection of the word lists of doc1 and doc2
    intersection = words_doc1.intersection(words_doc2)
    
    # Find the union of the word lists of doc1 and doc2
    union = words_doc1.union(words_doc2)
    
    try:
        jsi = float(len(intersection)) / len(union)
    except ZeroDivisionError as zde:
        jsi = None
    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return jsi


def compute_precision(pred, true):
    try:
        true = true.split(',')
        true = [int(i) for i in true]
    except:
        true = None
    
    if pred is None and true is not None:
        precision = 0
        return precision

    try:
        set_of_pred = set(pred)
        set_of_true = set(true)
        intersect = len(set_of_pred.intersection(set_of_true))
        precision = round((intersect / len(set_of_pred)), 2)
    except:
        precision = 0

    return precision


def compute_recall(pred, true):
    try:
        true = true.split(',')
        true = [int(i) for i in true]
    except:
        true = None
    
    if pred is None and true is not None:
        recall = 0
        return recall

    try:
        set_of_pred = set(pred)
        set_of_true = set(true)
        intersect = len(set_of_pred.intersection(set_of_true))
        recall = round((intersect / len(set_of_true)), 2)
    except:
        recall = 0

    return recall


def compute_f1(precision, recall):
    try:
        f1 = (2 * precision * recall) / (precision + recall)
    except:
        f1 = 0

    return f1


def evaluate_articles_of_law(df):
    pre_length = len(df)
    df = df.dropna(subset=['articles_y'])  # remove the nan's
    post_length = len(df)

    print(f'We dropped {pre_length - post_length} rows because of NaN values.')

    df['articles_precision'] = df.apply(lambda x: compute_precision(x.articles_x, x.articles_y), axis=1)
    df['articles_recall'] = df.apply(lambda x: compute_recall(x.articles_x, x.articles_y), axis=1)
    
    return df


def evaluate_tables(df):
    df['tables_precision'] = df.apply(lambda x: compute_precision(x.table_pages_x, x.table_pages_y), axis=1)
    df['tables_recall'] = df.apply(lambda x: compute_recall(x.table_pages_x, x.table_pages_y), axis=1)

    return df


def evaluate_tables_no_rules(df):
    df['tables_precision'] = df.apply(lambda x: compute_precision(x.table_pages_x_no_rules, x.table_pages_y), axis=1)
    df['tables_recall'] = df.apply(lambda x: compute_recall(x.table_pages_x_no_rules, x.table_pages_y), axis=1)

    return df


def evaluate(df1, df2, nlp):
    df = pd.merge(df1, df2, how='right', on='file_name')

    print(f'There are {len(df[df.letter == 0])} non-Wob documents found, we remove those.')
    df = df[df.letter != 0]

    print(f'There are {len(df[df.image_based == 1])} (partly) image-based documents found, we remove those.')
    df = df[df.image_based != 1]

    print(f'The final shape of the dataframe is: {df.shape}')

    # decision date and request date
    df['decision_date_equal'] = df.apply(lambda x: is_equal(x.decision_date_x, x.decision_date_y), axis=1)
    df['request_date_equal'] = df.apply(lambda x: is_equal(x.request_date_x, x.request_date_y), axis=1)
    
    # # decision and request
    df['lemm_dec_x'] = df['decision_x'].apply(lambda x: lemmatizer(x, nlp))
    df['lemm_dec_y'] = df['decision_y'].apply(lambda x: lemmatizer(x, nlp))
    df['lemm_req_x'] = df['request_x'].apply(lambda x: lemmatizer(x, nlp))
    df['lemm_req_y'] = df['request_y'].apply(lambda x: lemmatizer(x, nlp))

    df['jacc_req'] = df.apply(lambda x: jaccard_similarity(x.lemm_req_x, x.lemm_req_y), axis=1)
    df['jacc_dec'] = df.apply(lambda x: jaccard_similarity(x.lemm_dec_x, x.lemm_dec_y), axis=1)

    # articles of law
    df['articles_precision'] = df.apply(lambda x: compute_precision(x.articles_x, x.articles_y), axis=1)
    df['articles_recall'] = df.apply(lambda x: compute_recall(x.articles_x, x.articles_y), axis=1)
    df['articles_f1'] = df.apply(lambda x: compute_f1(x.articles_precision, x.articles_recall), axis=1)
    df['articles_f1'] = df.apply(lambda x: 0 if np.isnan(x['articles_f1']) else x['articles_f1'], axis=1)

    # tables
    df['tables_precision'] = df.apply(lambda x: compute_precision(x.table_pages_x, x.table_pages_y), axis=1)
    df['tables_recall'] = df.apply(lambda x: compute_recall(x.table_pages_x, x.table_pages_y), axis=1)
    df['tables_f1'] = compute_f1(df.tables_precision, df.tables_recall)
    df['tables_f1'] = df.apply(lambda x: 0 if np.isnan(x['tables_f1']) else x['tables_f1'], axis=1)

    # tables no rules
    df['tables_precision_no_rules'] = df.apply(lambda x: compute_precision(x.table_pages_no_rules, x.table_pages_y), axis=1)
    df['tables_recall_no_rules'] = df.apply(lambda x: compute_recall(x.table_pages_no_rules, x.table_pages_y), axis=1)
    df['tables_f1_no_rules'] = compute_f1(df.tables_precision_no_rules, df.tables_recall_no_rules)
    df['tables_f1_no_rules'] = df.apply(lambda x: 0 if np.isnan(x['tables_f1_no_rules']) else x['tables_f1_no_rules'], axis=1)

    return df


def score(df, output_folder, dataset):
    
    print("\n")
    print(f"##### SCORING THE DATES ({dataset}) #####")
    print("> The decision date:")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['decision_date_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    true_decision_dates = data['decision_date_equal'].value_counts().loc[True]

    true_decision_percentage = round((true_decision_dates / post_length * 100), 2)

    print(f'The ACCURACY for the decision date is {true_decision_percentage} %')

    ##############################################################################

    print("\n")
    print("> The request date:")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['request_date_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    true_request_dates = data['request_date_equal'].value_counts().loc[True]

    true_request_percentage = round((true_request_dates / post_length * 100), 2)

    print(f'The ACCURACY for the request date is {true_request_percentage} %')

    ##############################################################################

    print("\n")
    print(f"##### SCORING THE DECISION AND REQUEST ({dataset}) #####")
    print("> The decision:")

    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['decision_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    jacc_dec_mean = round((data.jacc_dec.mean() * 100), 2)

    print(f'The mean of the JACCARD SIMILARITY INDEX for the decision is {jacc_dec_mean} %')

    sns.displot(data['jacc_dec'], kde=False, color='blue', bins=50)
    plt.title(f'Distribution of Jaccard Similarity Index for the decision ({dataset})', fontsize=14)
    plt.xlabel('Jaccard Similarity Index', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig(f'{output_folder}/Distribution of Jaccard Similarity Index for the decision ({dataset}).png', dpi=300)
    plt.show()
    plt.clf()

    ##############################################################################

    print("\n")
    print("> The request:")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['request_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    jacc_req_mean = round((data.jacc_req.mean() * 100), 2)

    print(f'The mean of the JACCARD SIMILARITY INDEX for the request is {jacc_req_mean} %')

    sns.displot(data['jacc_req'], kde=False, color='blue', bins=50)
    plt.title(f'Distribution of Jaccard Similarity Index for the request ({dataset})', fontsize=14)
    plt.xlabel('Jaccard Similarity Index', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig(f'{output_folder}/Distribution of Jaccard Similarity Index for the request ({dataset}).png', dpi=300)
    plt.show()
    plt.clf()

    ##############################################################################

    print("\n")
    print(f"##### SCORING THE ARTICLES OF LAW ({dataset}) #####")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['articles_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    articles_precision_mean = round((data.articles_precision.mean() * 100), 2)
    articles_recall_mean = round((data.articles_recall.mean() * 100), 2)
    articles_f1_mean = round((data.articles_f1.mean() * 100), 2)

    print(f'The mean of the PRECISION for the articles of law is {articles_precision_mean} %')
    print(f'The mean of the RECALL for the articles of law is {articles_recall_mean} %')
    print(f'The mean of the F1 for the articles of law is {articles_f1_mean} %')

    ##############################################################################

    print("\n")
    print(f"##### SCORING THE TABLES ({dataset}) #####")
    print("> With rules")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['table_pages_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    tables_precision_mean = round((data.tables_precision.mean() * 100), 2)
    tables_recall_mean = round((data.tables_recall.mean() * 100), 2)
    tables_f1_mean = round((data.tables_f1.mean() * 100), 2)

    print(f'The mean of the PRECISION for the tables is {tables_precision_mean} %')
    print(f'The mean of the RECALL for the tables is {tables_recall_mean} %')
    print(f'The mean of the F1 for the tables is {tables_f1_mean} %')

    #############################################################################

    print("\n")
    print("> Without rules")
    data = df.copy()
    pre_length = len(data)
    data = data.dropna(subset=['table_pages_y'])
    post_length = len(data)
    print(f"We removed {pre_length - post_length} records due to NaN values. We are left with {post_length} records.")

    tables_precision_no_rules_mean = round((data.tables_precision_no_rules.mean() * 100), 2)
    tables_recall_no_rules_mean = round((data.tables_recall_no_rules.mean() * 100), 2)
    tables_f1_no_rules_mean = round((data.tables_f1_no_rules.mean() * 100), 2)

    print(f'The mean of the PRECISION for the tables is {tables_precision_no_rules_mean} %')
    print(f'The mean of the RECALL for the tables is {tables_recall_no_rules_mean} %')
    print(f'The mean of the F1 for the tables is {tables_f1_no_rules_mean} %')
