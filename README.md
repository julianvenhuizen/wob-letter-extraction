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

## Extracting the features

Every step of the feature extracting process is set out and explained in the ["Feature extraction on Wob decision letters" notebook](https://github.com/julianvenhuizen/wob-letter-extraction/blob/99eb23cc8749560ddafc3955172ce4a9a9c53524/Feature%20extraction%20on%20Wob%20decision%20letters.ipynb). 

To run the notebook, you will only need a folder containing machine-readable (text-based, not image-based) Wob decision letters in PDF. In addition to this, the classifyer can work as a safety-net, only extracting text from documents that contain a higher percentage of text than the set threshold.

## Evaluating with ground truth

The extracted features can be evaluated against the ground truth in CSV file format. The [ground truth folder](https://github.com/julianvenhuizen/wob-letter-extraction/tree/main/data/GT) shows examples of CSV files containing the ground truth. Your own, unique CSV file should contain the same columns and column names.
