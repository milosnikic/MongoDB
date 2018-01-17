"""
** POJEKAT      : predmet Elektronsko poslovanje
** NAZIV        : MongoDB
** OPIS         :     Kreiranje konzolne aplikacije.
**                    Implementacija najosnovnijih operacija
**                    za rad sa nerelacionim bazama podataka.
**                    Moguce je dodavati zapise, brisati,
**                    ispisivati, sortirati, kao i pretrazivati na
**                    osnovu zadatih atributa.
** VERZIJA      : 1.0
**
** DATUM: 17.1.2018.
**
** Copyright (C) Miloš Nikić, Miloš Mirković 2018.
"""

from pymongo import *
import pprint

def collection(db):
    #Izmedju kolekcija i tabela(u relacionim bazama) moze
    #da se uspostavi odredjena analogija
    #Na ovaj nacin kreirali smo kolekciju sa
    #zeljenim nazivom
    return db.coll

'''
Metoda za ispis recorda
'''
def get_all(coll):
    #Metoda find() vraca sve zapise, poput SELECT * u SQL
    #Na ovaj nacin ispisujemo sve zapise u kolekciji
    records = coll.find()
    if records.count() == 0:
        print('\nKolekcija je prazna.\n\n')
    else:
        for instance in records:
            pprint.pprint(instance)
'''
Metoda koja se koristi za popunjavanje atributa i vraca recnik
'''
def attribute_fill(coll):
    record = dict()
    print('UKOLIKO JE ATRIBUT INTEGER, POSLE NAZIVA ATRIBUTA DODATI :INT, ZA DOUBLE DODATI :DOUBLE')
    print('PRIMER: godiste:INT, temperatura:DOUBLE')
    print("ZA PREKID UNOSA ATRIBUTA UNESITE 'q'")
    unos = input('Unesite zeljeni atribut: ')
    keys = []
    while unos != 'q':
        keys.append(unos)
        unos = input('Unesite zeljeni atribut: ')
    if len(keys) > 0:
        for key in keys:
            if key.find(':INT') != -1:
                print('integer')
                key = key.split(':')[0]
                value = int(input('Unesite vrednost za atribut -{}-: '.format(key)))
                record[key]=value
            elif key.find(':DOUBLE') != -1:
                print('double')
                key = key.split(':')[0]
                value = float(input('Unesite vrednost za atribut -{}-: '.format(key)))
                record[key]=value
            else:
                print('string')
                value = input('Unesite vrednost za atribut -{}-: '.format(key))
                record[key]=value
    return record

'''
Unosenje odredjenog rekorda sa varijabilnim brojem atributa
'''
def add(coll):
        record = attribute_fill(coll)
        coll.insert_one(record)

'''
Unosenje vise od jednog rekorda
'''
def add_many(coll):
    more = True
    while more:
        add(coll)
        dec = input('Zelite li jos recorda da ubacite? ')
        if dec in ('ne','Ne','nE','NE'):
            more = False

'''
Prikazivanje sortiranih podataka na osnovu unetih atributa
'''
def sort_by(coll):
    records = []
    attrbs = []
    print('PRETPOSTAVLAJ SE DA KORISNIK UNOSI VALIDNE ATRIBUTE')
    print('TJ. NE UNOSI NEPOSTOJECE ATRIBUTE')
    print("ZA PREKID UNOSA ATRIBUTA UNESITE 'q'")
    unos = input('Unesite zeljeni atribut: ')
    while unos != 'q':
        attrbs.append(unos)
        unos = input('Unesite zeljeni atribut: ')
    if len(attrbs) > 0:
        for attribute in attrbs:
            print('a) Rastuce')
            print('b) Opadajuce')
            pref = input('Unesite r ili o:')
            #Za sortiranje rastuce kao drugi parametar u funkciju sort
            #potrebno je proslediti 1, a za opadajuci redosled -1
            if pref == 'r':
                record = (attribute, 1)
                records.append(record)
            elif pref == 'o':
                record = (attribute, -1)
                records.append(record)
            else:
                print('Pogresan unos za direkciju.')
        for item in coll.find().sort(records):
            pprint.pprint(item)


'''
Brisanje svih zapisa iz kolekcije
'''
def remove_all(coll):
    #Pristupanje svakom pojedinacnom zapisu i njegovo brisanje
    for record in coll.find():
        coll.remove(record)

'''
Brisanje odredjenih zapisa iz kolekcije
'''
def remove(coll):
    print('UNESITE ATRIBUTE, KAKO BISMO IZBRISALI ZAPIS')
    record = attribute_fill(coll)
    coll.remove(record)

'''
Pretrazivanje kolekcije na osnovu zadatih atributa
'''
def search(coll):
    record = attribute_fill(coll)
    records = coll.find(record)
    if records.count() == 0:
        print("Ne postoji takav zapis!")
    else:
        for item in records:
            pprint.pprint(item)

'''
Ispis glavnog menija
'''
def show():
    string = '''\tABOUT:\n\tAplikacija omogucuje osnovne operacije\n\tkoje podrzavaju sve aplikacije slicnog tipa.
    \n\tOmogucen je unos pojedinacnog zapisa, kao i visestruki unos.\n\tTakodje omogucena je pretraga po zeljenim atributima.
    \n\tMoguce je izvrsiti sortiranje na osnovu bilo kog atributa.\n\tMoguce je izbrisati pojedinacni zapis,\n\tkao i sve zapise iz kolekcije.'''
    print('*' * 80)
    print('\tDobrodosli u aplikaciju')
    print('\tza manipulaciju bazom podataka')
    print('*' * 80)
    print('\tRadi lakseg koriscenja baza se inicjalizuje automatski\n\tkao i kolekcija u koju se dodaju zapisi')
    print('*' * 80)
    print(string)
    print('*' * 80)
    print('\tCopyright (C) Miloš Nikić, Miloš Mirković 2018.')



'''
Glavni program
'''
def main(con):
    #Potrebno je izvrsiti kreiranje baze podataka
    #kako bismo bilo sta mogli da radimo.
    #Baza i kolekcije nisu napravljene na serveru
    #njihvo kreiranje se vrsi kada se prvi dokument ubaci
    #Baza podataka
    db = con.database
    #Kolekcija
    coll = collection(db)
    show()
    print('\n'*3)
    while True:
        print('1) Unesite jedan zapis')
        print('2) Unesite vise zapisa')
        print('3) Ispis svih zapisa kolekcije')
        print('4) Sortirajte prema atributu')
        print('5) Brisanje svih zapisa u kolekciji')
        print('6) Brisanje zapisa na osnovu atributa')
        print('7) Pretrazivanje na osnovu atributa')
        print('*****q za izlaz*****')
        choice = input('Unesite zeljenu opciju: ')
        if choice == '1':
            add(coll)
        elif choice == '2':
            add_many(coll)
        elif choice == '3':
            get_all(coll)
        elif choice == '4':
            sort_by(coll)
        elif choice == '5':
            remove_all(coll)
        elif choice == '6':
            remove(coll)
        elif choice == '7':
            search(coll)
        elif choice in ('q','Q','quit','quit'.upper()):
            print('Hvala na koriscenju nase aplikacije!')
            return
        else:
            print('Pogresan unos, pokusajte ponovo!')

if __name__ == '__main__':
    #Eksplicitno dodeljivanje adrese i porta
    #po defaultu bi se dodelila adresa lokalne masine
    #i odredjeni port 27017 koji je rezervisan za mongodb
    con = MongoClient('localhost',27017)
    main(con)
