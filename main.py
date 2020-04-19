import numpy as np
import pandas as pd
from flask import Flask, render_template,request
import test
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def retrieval(result):
    file = open("Daftar-Resep-Makanan.txt", encoding="utf8")
    soup = BeautifulSoup(file, 'html.parser')

    doc_makanan = soup.find_all("doc")

    documents = []
    for index in result:
        documents.append(doc_makanan[index])

    file.close()
    return documents

@app.route('/')
def dictionary():
    return render_template('home.html')

@app.route("/query", methods=['POST'])
def upload():
    start = time.time()
    query = request.form['query']

    result = test.process_query(query)

    documents = retrieval(result)

    # print(result)

    end = time.time()
    times = end - start

    return render_template('card.html', resep = documents, jlh_resep = len(documents), time = str(times) + " Seconds")


if __name__ == '__main__':
    app.run()