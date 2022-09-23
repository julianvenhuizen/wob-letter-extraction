import pdfplumber
import re
import spacy
from nltk.corpus import stopwords
from preparation import clean_text, split_in_sentences


def from_dict_to_sentences(dictionary):
    """
    Gets a dictionary of sentences.
    """

    clean_dictionary = {k: clean_text(v) for k, v in dictionary.items()}
    sentences = {k: split_in_sentences(v) for k, v in clean_dictionary.items()}
    
    return sentences


def get_sentences_with_thesaurus_words(sentences, key_word, page_no):
    """
    Retrieves the sentences that contain a (synonym) of the key word.
    """

    instance = Wn_grid_parser(Wn_grid_parser.odwn)
    synonyms = instance.les_lemma_synonyms(key_word)
    sentences_list = []
    
    try:
        for sentence in sentences[page_no]:
            i = sentences[page_no].index(sentence)
            if any(word in sentence for word in synonyms):
                sentences_list.append(sentence)
    except:
        pass
            
    return sentences_list


def get_sentences_with_subtexts(sentences, subtexts):
    """
    Retrieves the sentences that contain a word in the subtexts list.
    """
    
    sentences_list = []
    
    try:
        for page in sentences:
            for sentence in page:
                if any(word in sentence for word in subtexts):
                    sentences_list.append(sentence)
    except:
        pass

    return sentences_list


def lemmatizer(texts):
    
    stopword_list = stopwords.words('dutch')
    nlp = spacy.load("nl_core_news_sm")

    texts = [text.replace("\n", "").strip() for text in texts]
    docs = nlp.pipe(texts)
    cleaned_lemmas = [[t.lemma_ for t in doc if t.lemma_ not in stopword_list] for doc in docs]
    
    return cleaned_lemmas


def get_decision(text):
    sentences = []
    for item in text:
        item = clean_text(item)
        sentences.append(split_in_sentences(item))

    subtexts = ['Ik besluit', 'Ik heb besloten']
    
    decision_list = get_sentences_with_subtexts(sentences, subtexts)
    decision = '.'.join(decision_list)
    decision = decision.strip()
    
    decision = re.sub(r'.+?(?=Ik)', '', decision)

    return decision


def get_request(text):
    txt_file = open("dutch_prepositions.txt", "r")
    file_content = txt_file.read()
    dutch_prepositions = file_content.split("\n")
    dutch_prepositions = dutch_prepositions[:-1] # remove final (empty preposition)
    dutch_prepositions.reverse() # reverse list to z-a so longer words get picked out first (inzake > in)
    txt_file.close()
        
    keywords = ['verzocht', 'verzoekt', 'vraagt', 'verzocht u', 'verzoekt u', 'vraagt u']
    subtexts = [k + ' ' + d for d in dutch_prepositions for k in keywords]
      
    request_list = []
    sentences = split_in_sentences(text[0])
        
    try:
        for sentence in sentences:
            if any((match := word) in sentence for word in subtexts):
                sentence = sentence.split(match, 1)[1]
                sentence = clean_text(sentence)
                sentence = sentence[:1].upper() + sentence[1:]
                request_list.append(sentence)
    except:
        pass
    
    request = '. '.join(request_list)
    
    return request
