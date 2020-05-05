import requests
from bs4 import BeautifulSoup
import numpy as np

pages = np.arange(1, 9, 1)


norut = 1
for page in pages:

    URL = "https://resepkoki.co/category/ayam/page/" + str(page)
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')
    weblinks = soup.find_all('div', class_="gr-i")
    # print(weblinks)

    pglinks = []

    for divs in weblinks:
        url = divs.find_all('a')[0].get('href')
        pglinks.append(url)

        # print(pglinks)

        file = open('Daftar-Resep-Makanan-Makanan.txt', 'a+')

    for link in pglinks:
        partext = []
        url = link
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Get Link Gambar
        gambar = soup.find('div', class_="awr-i").find_all('img')[0].get('data-lazy-src')
        
        # Get Nama Makanan
        nama = soup.find(class_="entry-title").get_text()

        # Get Bahan
        bahan = soup.find('div', class_="awr-i").find_all('li')

        for x in bahan:
            if x.find_parent("ul"):
                partext.append(x.get_text())
            
        new_recipe = soup.new_tag('DOC')
        id_makanan = soup.new_tag('ID')
        id_makanan.string = "AYAM " + str(norut)
        link_gambar = soup.new_tag('LINK')
        link_gambar.string = gambar
        nama_makanan = soup.new_tag('NAMA')
        nama_makanan.string = nama
        bahan_makanan = soup.new_tag('BAHAN')
        bahan_makanan.string = ". ".join(partext)
        doc_arr = [id_makanan, link_gambar, nama_makanan, bahan_makanan]

        for x in doc_arr:
            new_recipe.append(x)

        file.write(new_recipe.prettify()+'\n')
        norut += 1

file.close()