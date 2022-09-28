import spacy
import re

from scripts.dates import get_dates
from scripts.reqdec import get_request, get_decision
from scripts.articles import get_articles
from scripts.tables import get_table_pages, get_table_pages_no_rules


def extract_features(df, nlp):
	"""
	Extracts the 6 features.
	"""

	df['decision_date'], df['request_date'] = zip(*df['clean_text'].apply(lambda x: get_dates(x, nlp)))
	df['request'] = df['clean_text'].apply(get_request)
	df['decision'] = df['clean_text'].apply(get_decision)
	df['articles'] = df['clean_text'].apply(get_articles)
	df['table_pages'] = df.apply(lambda x: get_table_pages(x.path, x.clean_text), axis=1)
	df['table_pages_no_rules'] = df.apply(lambda x: get_table_pages_no_rules(x.path, x.clean_text), axis=1)

	return df
