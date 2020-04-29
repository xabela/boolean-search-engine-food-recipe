import numpy as np
import pandas as pd
from flask import Flask, render_template,request
import test
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

documents = {}
len_all_docs = 0

def retrieval(result):
    file = open("Daftar-Resep-Makanan-Dengan-Bahan.txt", encoding="utf8")
    soup = BeautifulSoup(file, 'html.parser')

    doc_makanan = soup.find_all("doc")

    global len_all_docs 
    len_all_docs = len(doc_makanan)

    global documents
    documents.clear()
    if (result):
        for index in result:
            ind = doc_makanan[index]
            doc_makanan_nama = ind.find("nama").get_text()
            doc_makanan_bahan = ind.find("bahan").get_text()
            documents.setdefault(doc_makanan_nama,doc_makanan_bahan)
    else:
        documents = {}
        
    file.close()
    return documents

@app.route('/')
def dictionary():
    return render_template('home.html')

@app.route("/query", methods=['POST'])
def upload():
    global documents
    start = time.time()
    query = request.form['query']

    result = test.process_query(query)
    documents.clear()
    documents = retrieval(result)

    # print(result)

    end = time.time()
    times = end - start

    return render_template('card.html', resep = documents, jlh_resep = len(documents), time = str(times) + " Seconds", jlh_docs = len_all_docs)


if __name__ == '__main__':
    app.run()
