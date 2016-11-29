from reuters_parser import ReutersParser
from nltk.corpus import stopwords
import string
import nltk
import os

DATA_DIR = "reuters-dataset"

def get_ignored_tokens():
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    return stop_words | punctuation

def remove_stop_words_and_punc(doc):
    ignored_tokens = get_ignored_tokens()
    return [word for word in nltk.word_tokenize(doc) if word not in ignored_tokens]

def stem_doc(doc):
    stemmer = nltk.stem.SnowballStemmer("english")
    return [stemmer.stem(word) for word in doc]

def get_docs():
    print "Loading documents..."
    docs = []
    parser = ReutersParser()
    files = os.listdir(DATA_DIR)
    for f in files:
        with open(DATA_DIR  + "/" + f) as open_file:
            for doc in parser.parse(open_file):
                docs.append(doc)
    return docs
