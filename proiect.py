import re

import requests
from bs4 import BeautifulSoup
from re import findall

URL = "https://www.biziday.ro/category/stiri/"
HEADERE = {"User-Agent": "curs-python-scraping/1.0 (exercitiu educativ, contact: curs@exemplu.ro)"}

TIPAR_METADATA = re.compile(
    r"([A-ZĂÂÎȘȚ][\wăâîșțĂÂÎȘȚ]*)\s*·\s*(\d{4}-\d{2}-\d{2})\s*@\s*(\d{2}:\d{2}:\d{2})\s*$"
)
def descompune_stirea(text, href):
    text = text.strip()
    potrivire = TIPAR_METADATA.search(text)
    if potrivire is None:
        return None

    sursa = potrivire.group(1)
    data = potrivire.group(2)
    ora = potrivire.group(3)
    continut = text[:potrivire.start()].strip()

    if not continut:
        return None

    return {"text": continut, "sursa": sursa, "data": data, "ora": ora, "url": href}

def stiri_de_pe_pagina(url):
    r = requests.get(url, headers=HEADERE, timeout=10)
    r.raise_for_status()
    stiri = BeautifulSoup(r.text, "lxml")
    titluri_stiri = stiri.select("a")
    lista_stiri = []
    for titlu in titluri_stiri:
        t = descompune_stirea(titlu.text, titlu.get("href"))
        if t:
            lista_stiri.append(t)
    return lista_stiri

def stiri_dupa_sursa(stiri, sursa):
    lista_noua = []
    for stire in stiri:
        if stire["sursa"].lower() == sursa.lower():
            lista_noua.append(stire)
    return lista_noua

def sursa_cea_mai_frecventa(stiri):
    dictionar_surse = {}
    if not stiri:
        return None
    for stire in stiri:
        if stire["sursa"] in dictionar_surse:
            dictionar_surse[stire["sursa"]] += 1
        else:
            dictionar_surse[stire["sursa"]] = 1
    sursa_frecventa = max(dictionar_surse, key = lambda values: dictionar_surse[values])

    return sursa_frecventa, dictionar_surse[sursa_frecventa]
def raport(n):
    ...
    stiri_pagina = stiri_de_pe_pagina(URL)
    frecventa = sursa_cea_mai_frecventa(stiri_pagina)
    text_returnat = f"Radar Biziday (primele {n} din {len(stiri_pagina)} stiri):"
    for index in range(1, n+1):
        text_stire_curenta = f"\n  {index}. [{stiri_pagina[index - 1]["data"]} {stiri_pagina[index - 1]["ora"]}] {stiri_pagina[index - 1]["text"]} ({stiri_pagina[index - 1]["sursa"]})"
        text_returnat = text_returnat + text_stire_curenta
    text_despre_frecventa = f"\nSursa cea mai frecventa: {frecventa[0]} ({frecventa[1]}de stiri)"
    text_returnat = text_returnat + text_despre_frecventa
    return text_returnat
print(raport(5))
