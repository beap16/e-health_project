import urllib.request
import re
from bs4 import BeautifulSoup

#CREO LA CLASSE paper CHE CONTIENE INFORMAZIONI BASE PER OGNI DOCUMENTO
class paper:
    id = 0
    title = ''
    abstract = ''
    score = 0

    def __init__(self, codice):
        self.id = codice

    def SetTitle(self,titolo):
        self.title = titolo

    def addAbstract(self, testo):
        self.abstract = testo

    def addScore(self, punteggio):
        self.score = punteggio

all_papers = []

#CERCO TUTTI I CODICI PUBID DI PAPER CONNESSI ALL'AMBITO DI RICERCA INTERESSATO
search_codes = urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cardiology+app&retmode=xml&RetMax=2')
codes = re.findall(r"<Id>.*?</Id>", str(search_codes.read()))
for code in codes:
    code = code.split('<Id>')
    code = code[1].split('</Id>')
    code = code[0]
    #print(code)
    all_papers.append(paper(code))
    #print(all_papers.__len__())



#QUI CERCO E SALVO GLI ABSTRACT E I TITOLI DI TUTTI I PAPER TROVATI
for p in all_papers:
    link = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=" + str(p.id) + "&retmode=xml"
    request_url = urllib.request.urlopen(link)
    # TIRIAMO FUORI L'ABSTRACT
    soup = BeautifulSoup(request_url.read(), 'html.parser')
    p.addAbstract(str(soup.abstract))
    titolo = str(soup.title).split('<title>')
    titolo = titolo[1].split('</title>')
    titolo = titolo[0]
    p.SetTitle(titolo)



#CREO E SETTO IL DIZIONARIO
dictionary = {}
file = open("Cardiology.txt", "r")
i=1
for line in file:
    line_separata = line.split('|')
    line_separata = line_separata[1]
    line_separata = line_separata.split('\n')
    value = str(i)
    #print(value)
    dictionary[value] = line_separata[0]
    i=i+1
file.close()


#PROCEDO ALL'ANALISI DELLA RICORRENZA DELLE PAROLE DEL DIZIONARIO ALL'INTERNO DEI PAPER
for p in all_papers:
    points = 0
    print(str(p.id))
    print(p.title)
    for word in dictionary:
        #HO MESSO TUTTO IN MAIUSCOLO PERCHE' LA FUNZIONE count() E' CASE SENSITIVE
        found_words = str(p.abstract).upper().count(dictionary[word].upper())
        points = points+found_words
        if(found_words>0):
            print(dictionary[word])
        #print(points)
    p.addScore(points)
    print(str(p.score))
    #Il punteggio percentuale l'ho settato per l'intervallo [5,30]
    if(points<=5):
        perc = 0
    else:
        perc = round(points/30*100)
    print('Questo paper tratta di cardiologia al ' + str(perc) + '%' + '\n\n')