# Feature extraction on _Wet openbaarheid bestuur_ (Wob) decision letters

Julián Venhuizen (julian.venhuizen@student.uva.nl)

The aim of this study is to research and apply knowledge extraction methods for multiple features of the Wob decision letter. While the decision letters usually follow the same structure, there are some differences to be found. These differences are mainly due to administrative bodies varying in the way they draft these letters.

There are six features that are commonly found in the letters, namely: the document list, the relevant articles of law, the request of the applicant, the final decision by the administrative body, the date of the decision and the date of the request. These features each warrant their own way of extraction and method of evaluation. For example, the document list is often a table and can be extracted by algorithmic table detection. The articles of law, on the other hand, can be obtained by using rule-based text extraction. The request and decision parts of the letter can be extracted using text segmentation. Finally, the dates relating to the request, decision and proceedings can be obtained using named-entity recognition. Figure 1 shows an example of a standard Wob decision letter, with the features highlighted.

<figure style="margin-top: 20px;">
    <img src="img/Annotated Wob decision letter.png" alt="Wob decision letter (annotated)"/>
    <figcaption style="margin: 20px 60px; text-align: center;">
        <strong><em>Figure 1. An annotated Wob decision letter showing the features we want to extract. Red: date of decision. Orange: date of request. Yellow: request. Green: decision. Blue: articles of law. Purple: inventory table.</em></strong>
    </figcaption>
</figure>

## Installing

(Optionally) Install ```virtualenv``` and create a virtual environment to keep things clean:

```
# create a virtual environment
pip install virtualenv 
virtualenv venv
source venv/bin/activate
```

(Optionally) When using a virtual environment, install ```ipykernel``` for Jupyter:

```
# install ipykernel
pip install ipykernel
python -m ipykernel install --user --name=venv
```

The recommended way to install the repo is shown below, which should install and handle all dependencies:

```
# clone the repo
git clone https://github.com/julianvenhuizen/wob-letter-extraction.git
cd wob-letter-extraction

# install python dependencies:
pip install -r requirements.txt
```

You will also need to download the NLTK stopwords corpus and the [spaCy model](https://spacy.io/usage/models). For efficiency you can download the small model: ```nl_core_news_sm```. However, for accuracy and to reproduce the results from the thesis, you are advised to download the large model:  ```nl_core_news_lg```.

```
# download NLTK stopwords
python -m nltk.downloader stopwords

# download spaCy model
python -m spacy download nl_core_news_lg
```

Now you can start up the notebook. Don't forget to select the correct kernel (venv):
```
# launch the notebook
jupyter notebook Feature_extraction_on_Wob_decision_letters.ipynb
```

## Extracting the features

Every step of the feature extracting process is set out and explained in the ["Feature extraction on Wob decision letters" notebook](https://github.com/julianvenhuizen/wob-letter-extraction/blob/071cde0c5db78a025856abbb66456d742e699c09/Feature_extraction_on_Wob_decision_letters.ipynb). 

To run the notebook, you will only need a folder containing machine-readable (text-based, not image-based) Wob decision letters in PDF. In addition to this, the classifyer can work as a safety-net, only extracting text from documents that contain a higher percentage of text than the set threshold.

## Evaluating with ground truth

The extracted features can be evaluated against the ground truth in CSV file format. The [ground truth folder](https://github.com/julianvenhuizen/wob-letter-extraction/tree/main/data/GT) shows examples of CSV files containing the ground truth. Your own, unique CSV file should contain the same columns and column names.
