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

# print(len(docs_makanan))
# for x in docs_makanan:
#     if x[1] != "":
#         docs_makanan_with_bahan.append(x)
# print(docs_makanan[:3])
# print(docs_makanan_with_bahan[:3])

docs_makanan_with_bahan = [word for word in docs_makanan if word[1] != ""]
splitted_docs_makanan_with_bahan = []
for doc in docs_makanan_with_bahan:
    splitted_docs_makanan_with_bahan.append(' '.join(doc).split())

semua_bahan = [word for doc in splitted_docs_makanan_with_bahan for word in doc]

# print(semua_bahan[:])
# print(len(semua_bahan))
# print(splitted_docs_makanan_with_bahan[:2][:])
bahan_unik = []
for bahan in semua_bahan:
    if bahan not in bahan_unik:
        bahan_unik.append(bahan)
# print(bahan_unik[:10])
# print(len(bahan_unik))

incidence_matrix = [[int(doc.count(un) > 0) for doc in splitted_docs_makanan_with_bahan] for un in bahan_unik]
inc_pandas = (pd.DataFrame(incidence_matrix, index = bahan_unik))
print(inc_pandas)
print(list(inc_pandas.values[:,0])) #dokumen pertama tok
print(list(inc_pandas.values[0, :])) #token pertama tok
# print(incidence_matrix[:0])

tes = input('insert your query: ')
inside_parentheses = tes[tes.find("(")+1:tes.find(")")]
inside_token = inside_parentheses.split(" ")

inside_keyword = []
inside_operator = []

for words in inside_token:
    if words.lower() != "and" and words.lower() != "or" and words.lower() != "not":
        inside_keyword.append(words.lower())
    else:
        inside_operator.append(words.lower())

query_without_parentheses = re.sub("[\(\[].*?[\)\]]", "", tes)
query_token = query_without_parentheses.split(" ")

outside_keyword = []
outside_operator = []

for words in query_token:
    if words.lower() != "and" and words.lower() != "or" and words.lower() != "not":
        outside_keyword.append(words.lower())
    else:
        outside_operator.append(words.lower())

for words in outside_operator:
    for i in range(len(docs_makanan_with_bahan)):
        index_kata_1 = bahan_unik.index(outside_keyword[0].lower())
        index_kata_2 = bahan_unik.index(outside_keyword[1].lower())
        if words.lower() == "and":
            if list(inc_pandas.values[:,i])[index_kata_1] == 1 and list(inc_pandas.values[:,i])[index_kata_2] == 1:
                print(docs_makanan_with_bahan[i])
        elif words.lower() == "or":
            if list(inc_pandas.values[:,i])[index_kata_1] == 1 or list(inc_pandas.values[:,i])[index_kata_2] == 1:
                print(docs_makanan_with_bahan[i])
        # elif words.lower() == "not":
        #     if outside_keyword[0] in splitted_docs_makanan_with_bahan[i][:] and outside_keyword[1] not in splitted_docs_makanan_with_bahan[i][:]:
        #         print(splitted_docs_makanan_with_bahan[i][:])

# print(keyword)
# print(operator)
# tes_A = splitted_docs_makanan_with_bahan
# for i in range(len(splitted_docs_makanan_with_bahan)):
#     if tes in tes_A[i][:]:
#         print(splitted_docs_makanan_with_bahan[i][:])
print("Program end at = ", datetime.now().time())