# R. Yudo Arya Kusuma
# 20051397013

import pandas as pd

#====================================Fuzzification====================================
#Function untuk menghitung nilai
def pelayananBuruk(nilai_pelayanan):
    if (nilai_pelayanan <=40):
        return 1
    elif (41 <= nilai_pelayanan <= 50):
        return (50 - nilai_pelayanan)/10
    else:
        return 0

def pelayananSedang(nilai_pelayanan):
    if (41 <= nilai_pelayanan <= 50):
        return (nilai_pelayanan - 40)/10
    elif (51 <= nilai_pelayanan <= 60):
        return 1
    elif (61 <= nilai_pelayanan <= 70):
        return (70 - nilai_pelayanan)/10
    else:
        return 0

def pelayananBaik(nilai_pelayanan):
    if (nilai_pelayanan >= 71):
        return 1
    elif (61 <= nilai_pelayanan <= 70):
        return (nilai_pelayanan - 60)/10
    else:
        return 0

def makananTidakEnak(nilai_makanan):
    if (nilai_makanan <=4):
        return 1
    elif (3 <= nilai_makanan <= 5):
        return (5 - nilai_makanan)/2
    else:
        return 0

def makananBiasa(nilai_makanan):
    if (3 <= nilai_makanan <= 5):
        return (nilai_makanan - 3)/2
    elif (5 <= nilai_makanan <= 7):
        return 1
    elif (7 <= nilai_makanan <= 9):
        return (9 - nilai_makanan)/2
    else:
        return 0

def makananEnak(nilai_makanan):
    if (nilai_makanan >= 8):
        return 1
    elif (6 <= nilai_makanan <= 8):
        return (nilai_makanan - 6)
    else:
        return 0

#Function untuk menampung nilai
def inBuruk(pelayanan):
    buruk = []
    for i in range(0,100):
        nilai = pelayanan[i]
        buruk.append(pelayananBuruk(nilai))
    return buruk

def inSedang(pelayanan):
    sedang = []
    for i in range(0,100):
        nilai = pelayanan[i]
        sedang.append(pelayananSedang(nilai))
    return sedang

def inBaik(pelayanan):
    baik = []
    for i in range(0,100):
        nilai = pelayanan[i]
        baik.append(pelayananBaik(nilai))
    return baik

def inTidakEnak(makanan):
    tidak_enak = []
    for i in range(0,100):
        nilai = makanan[i]
        tidak_enak.append(makananTidakEnak(nilai))
    return tidak_enak

def inBiasa(makanan):
    biasa = []
    for i in range(0,100):
        nilai = makanan[i]
        biasa.append(makananBiasa(nilai))
    return biasa

def inEnak(makanan):
    enak = []
    for i in range(0,100):
        nilai = makanan[i]
        enak.append(makananEnak(nilai))
    return enak

#====================================INFERENCE====================================
def tblMengecewakan(buruk, sedang, tidak_enak, biasa, enak):
    mengecawakan = []

    for i in range(0,100):
        mengecawakan.append(max(min(buruk[i], tidak_enak[i]), min(buruk[i], biasa[i]), min(buruk[i], enak[i]), min(sedang[i], tidak_enak[i]) ))
    return mengecawakan

def tblOK(sedang, baik, tidak_enak, biasa):
    ok = []

    for i in range(0,100):
        ok.append(max(min(sedang[i], biasa[i]), min(baik[i], tidak_enak[i]) ))
    return ok

def tblPuas(sedang, baik, biasa, enak):
    puas = []

    for i in range(0,100):
        puas.append(max(min(sedang[i], enak[i]), min(baik[i], biasa[i]), min(baik[i], enak[i]) ))
    return puas

 #====================================DEFUZZIFICATION====================================  
def defuzzSugeno(mengecewakan, ok, puas):
    defuzz = []
    
    for i in range(0,100):
        defuzz.append((mengecawakan[i]*50 + ok[i]*70 + puas[i]*100)/(mengecawakan[i] + ok[i] + puas[i]))
    return defuzz

#====================================HASIL AKHIR====================================
def isiTblAkhir(defuzz):
    tblAkhir = []

    for i in range(0,100):
        tampung = []
        tampung.append(i+1)
        tampung.append(defuzz[i])
        tblAkhir.append(tampung)
    return tblAkhir

def selectionSort(tblAkhir):
    for i in range(0,100):
        maks = i
        for j in range(i+1,100):
            if (tblAkhir[j][1] > tblAkhir[maks][1]):
                maks = j
            tblAkhir[maks], tblAkhir[i] = tblAkhir[i], tblAkhir[maks]

def top10(tblAkhir):
    tertinggi_10 = []
    for i in range(0,10):
        tertinggi_10.append(tblAkhir[i][0])
    return tertinggi_10

#====================================MAIN PROGRAM====================================
#Import xlsx
restoran = pd.read_excel('restoran.xlsx')
indeks = restoran['id'].tolist()
pelayanan = restoran['pelayanan'].tolist()
makanan = restoran['makanan'].tolist()

#Fuzzification
buruk = inBuruk(pelayanan)
sedang = inSedang(pelayanan)
baik = inBaik(pelayanan)
tidak_enak = inTidakEnak(makanan)
biasa = inBiasa(makanan)
enak = inEnak(makanan)

#Inference
mengecawakan = tblMengecewakan(buruk, sedang, tidak_enak, biasa, enak)
ok = tblOK(sedang, baik, tidak_enak, biasa)
puas = tblPuas(sedang, baik, biasa, enak)

#Defuzzification
defuzz = defuzzSugeno(mengecawakan, ok, puas)

#Hasil Akhir
tblAkhir = isiTblAkhir(defuzz)
selectionSort(tblAkhir)
tertinggi_10 = top10(tblAkhir)

#Export to xlsx
df = pd.DataFrame(tertinggi_10)
df.to_excel(r'peringkat.xlsx',index = False)


