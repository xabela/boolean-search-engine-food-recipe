from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from bs4 import BeautifulSoup
import text_preprocessing as pp
import csv
import re
from datetime import datetime
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

print("Program start at = ", datetime.now().time())

# factory = StemmerFactory()
# stemmer = factory.create_stemmer()
# file = open("Daftar-Resep-Makanan.txt", encoding="utf8")
# soup = BeautifulSoup(file, 'html.parser')

# doc_makanan = soup.find_all("doc")

# list_of_nama = []
# list_of_bahan = []
docs_makanan = []

# f = open('makanan.csv', 'w')
# writer = csv.writer(f)

# for makanan in doc_makanan:
#     a = makanan.find("nama").text
#     b = makanan.find("bahan").text
#     nama = pp.preprocessing(a)
#     bahan = pp.preprocessing(b)
# #     # token_nama = list_of_nama.append(nama)
# #     # token_bahan = list_of_bahan.append(bahan)
#     docs_makanan.append([nama, bahan])
#     writer.writerow([nama, bahan])

# print(docs_makanan)

with open('makanan.csv', 'r') as read_obj:
    reader = csv.reader(read_obj)
    docs_makanan = list(reader)

docs_makanan = list(filter(None,docs_makanan))

print(len(docs_makanan))

docs_makanan_with_bahan = []

for x in docs_makanan:
    if x[1] != "":
        docs_makanan_with_bahan.append(x)

# print(docs_makanan_with_bahan[:3])
splitted_docs_makanan_with_bahan = []
for doc in docs_makanan_with_bahan:
    splitted_docs_makanan_with_bahan.append(' '.join(doc).split())

semua_bahan = []
bahan_unik = []

for x in docs_makanan_with_bahan:
    bahan_array = x[1].split(" ")
    for words in bahan_array:
        semua_bahan.append(words)

print(len(semua_bahan))

for bahan in semua_bahan:
    if bahan not in bahan_unik:
        bahan_unik.append(bahan)

print(len(bahan_unik))
# print(bahan_unik)
# for x in docs_makanan:
#     if x == None:
#         docs_makanan.remove(x)
    # elif x[1] == "":
    #     docs_makanan.remove(x)

# print(len(docs_makanan))
incidence_matrix = [[int(doc.count(un) > 0) for doc in splitted_docs_makanan_with_bahan] for un in bahan_unik]
print(pd.DataFrame(incidence_matrix, index = bahan_unik))

# print(unik)

print("Program end at = ", datetime.now().time())