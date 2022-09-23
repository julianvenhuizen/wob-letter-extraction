import re 


def get_articles(text):
    i = 0
    articles = []
    while i <= 20:
        x = 'Artikel ' + str(i)
        articles.append(x)
        i += 1
        
    articles_in_text = []
    page_indexes = []
    for article in articles:
        for subtext in text: 
            if article in subtext:
                page_index = text.index(subtext)
                articles_in_text.append(articles.index(article))
                page_indexes.append(page_index)
    articles = list(dict.fromkeys(articles_in_text))
    
    return articles
