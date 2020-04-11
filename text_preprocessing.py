from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocessing(docs):
    cleaned = re.sub("[^a-zA-Z\s]+", " ", docs)
    # FOLDING WORDS
    folded = cleaned.lower()
    # TOKENIZING
    token = re.findall("[^\s0-9][A-Za-z]+", folded)
    string = " ".join(token)
    return stemmer.stem(string)