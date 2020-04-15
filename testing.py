


a = [['ayam','nasi','kopi'],['ayam','gula','kopi'],['ayam','gula','kopi']]

asds = 'ayam' and 'nasi' and 'kopi'

for i in range(len(a)):
    if asds in a[i][:]:
        print(a[i][:])

def inputan():
    logic = ['or','or)','(or','and','(and','and)',')','(']
    print('Halo Cari resep apa?')
    query = []
    query_temp = []
    inputana = ''
    counter = -1
    star = ''
    print('Ketik "search" untuk memulai mencari')
    while inputana != 'search':
        counter+=3
        inputana = input()
        if inputana == 'and':
            query.append('and')

        elif inputana == '(and':
            query.append('(and')

        elif inputana == 'and)':
            query.append('and)')

        elif inputana == 'or':
            query.append('or')

        elif inputana == '(or':
            query.append('(or')

        elif inputana == 'or)':
            query.append('or)')

        elif inputana == 'search':
            pass
        elif inputana != '':
            query.append(' "'+inputana+'"')
            query.append(' in tes_A[i][:] ')
        try:
            if query[0] in logic:
                print('Tidak boleh memasukan logika terlebih dahulu')
                query.clear()
            elif query[counter] not in logic:
                print('Harus memakai logic setelah kata')
                query.pop()
                query.pop()
                counter-=3
        except IndexError:
            counter -= 3
            pass
    for item in query:
        star+= item
    return star

