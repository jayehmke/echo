# import nltk
from nltk.stem import WordNetLemmatizer

# nltk.data.path.append('./nltk_data/')
wnl = WordNetLemmatizer()


def is_plural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma
