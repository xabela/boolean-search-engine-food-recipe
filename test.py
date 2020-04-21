from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from bs4 import BeautifulSoup
import text_preprocessing as pp
import csv
import re
from datetime import datetime
import pandas as pd
import collections

print("Program start at = ", datetime.now().time())

# factory = StemmerFactory()
# stemmer = factory.create_stemmer()
# file = open("Daftar-Resep-Makanan.txt", encoding="utf8")
# soup = BeautifulSoup(file, 'html.parser')

# doc_makanan = soup.find_all("doc")

# list_of_nama = []
# list_of_bahan = []

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

docs_makanan = []

with open('makanan.csv', 'r') as read_obj:
    reader = csv.reader(read_obj)
    docs_makanan = list(reader)

docs_makanan = list(filter(None,docs_makanan))

docs_makanan_with_bahan = [word for word in docs_makanan if word[1] != ""]
splitted_docs_makanan_with_bahan = []
for doc in docs_makanan_with_bahan:
    splitted_docs_makanan_with_bahan.append(' '.join(doc).split())

semua_bahan = [word for doc in splitted_docs_makanan_with_bahan for word in doc]

bahan_unik = []
for bahan in semua_bahan:
    if bahan not in bahan_unik:
        bahan_unik.append(bahan)

incidence_matrix = [[int(doc.count(un) > 0) for doc in splitted_docs_makanan_with_bahan] for un in bahan_unik]
inc_pandas = (pd.DataFrame(incidence_matrix, index = bahan_unik))

def postfix(infix_tokens):
    
    #precendence initialization
    prioritas = {'NOT':3, 'AND':2, 'OR':1, '(':0, ')':0} 

    output = []
    operator_stack = []
    
    #creating postfix expression
    for token in infix_tokens:
        if (token == '('):
            operator_stack.append(token)

        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        
        elif (token in prioritas):
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and prioritas[current_operator] > prioritas[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token)

        else:
            output.append(token.lower())
    
    #while stack is not empty appending
    while (operator_stack):
        output.append(operator_stack.pop())
    return output

docs_hasil_index = []
docs_hasil_inc = []

def AND_op(*word):
    if(len(word) == 1):
        for i in range(0, len(docs_hasil_index)):
            docs_list = list(inc_pandas.values[:,i])
            index_kata_1 = bahan_unik.index(word[0])
            if docs_hasil_inc[i][index_kata_1] == 1:
                docs_hasil_index.append(i)
    else:
        for i in range(0, len(docs_makanan_with_bahan)):
            docs_list = list(inc_pandas.values[:,i])
            index_kata_1 = bahan_unik.index(word[0])
            index_kata_2 = bahan_unik.index(word[1])
            if docs_list[index_kata_1] == 1 and docs_list[index_kata_2] == 1:
                docs_hasil_inc.append(docs_list)
                docs_hasil_index.append(i)

def OR_op(*word):
    if(len(word) == 1):
        for i in range(0, len(docs_hasil_index)):
            docs_list = list(inc_pandas.values[:,i])
            index_kata_1 = bahan_unik.index(word[0])
            if docs_list[index_kata_1] == 1:
                docs_hasil_index.append(i)
    else:
        for i in range(0, len(docs_makanan_with_bahan)):
            docs_list = list(inc_pandas.values[:,i])
            index_kata_1 = bahan_unik.index(word[0])
            index_kata_2 = bahan_unik.index(word[1])
            if docs_list[index_kata_1] == 1 or docs_list[index_kata_2] == 1:
                docs_hasil_inc.append(docs_list)
                docs_hasil_index.append(i)

def NOT_op(word):
    for i in range(len(docs_makanan_with_bahan)):
        docs_list = list(inc_pandas.values[:,i])
        index_kata_1 = bahan_unik.index(word)
        if docs_list[index_kata_1] == 0:
            docs_hasil_inc.append(docs_list)
            docs_hasil_index.append(i)

def OneQuery(word):
    for i in range(len(docs_makanan_with_bahan)):
        docs_list = list(inc_pandas.values[:,i])
        index_kata_1 = bahan_unik.index(word)
        if docs_list[index_kata_1] == 1:
            docs_hasil_inc.append(docs_list)
            docs_hasil_index.append(i)

def process_query(q):
    q = q.replace('(', '( ')
    q = q.replace(')', ' )')
    q = q.split(' ')
    query = []

    for i in q:
        query.append(i)
    for i in range(0,len(query)):
        if ( query[i]== 'and' or query[i]== 'or' or query[i]== 'not'):
            query[i] = query[i].upper()

    results_stack = []
    postfix_queue = postfix(query)

    if (len(postfix_queue) == 1):
        OneQuery(''.join(postfix_queue))
    else: 
        for i in postfix_queue:
            if ( i!= 'AND' and i!= 'OR' and i!= 'NOT'):
                i = i.replace('(', ' ')
                i = i.replace(')', ' ')
                i = i.lower()
                results_stack.append(i)
            elif (i=='AND'):
                if(len(results_stack) == 0):
                    temp = [item for item, count in collections.Counter(docs_hasil_index).items() if count > 1]
                    docs_hasil_index.clear()
                    for x in temp:
                        docs_hasil_index.append(x)
                elif(len(results_stack) == 1):
                    word = results_stack.pop()
                    AND_op(word)
                else:
                    a = results_stack.pop()
                    b = results_stack.pop()
                    AND_op(a, b)
            elif (i=='OR'):
                if(len(results_stack) == 0):
                    temp = list(set(docs_hasil_index))
                    docs_hasil_index.clear()
                    for x in temp:
                        docs_hasil_index.append(x)

                elif(len(results_stack) == 1):
                    word = results_stack.pop()
                    OR_op(word)

                else:
                    a = results_stack.pop()
                    b = results_stack.pop()
                    OR_op(a,b)
            elif (i == 'NOT'):
                c = results_stack.pop()
                print(c)
                NOT_op(c)

    return docs_hasil_index

print("Program end at = ", datetime.now().time())