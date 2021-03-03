
"""
    Avem aplicatia care tine stocul unui depozit (Cap 5-6). Efectuati urmatoarele imbunatatiri:
	
	Este necesar rezolvati minim 5 din punctele de mai jos:

1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o 
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa 
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--

4. Utilizati Regex pentru a cauta :
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
    Categoria
        - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
        - denc VARCHAR(255) (text in loc de varchar in sqlite3)
    Produs
        - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idc INT NOT NULL
        - denp VARCHAR(255)
        - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
        # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
    Operatiuni
        - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idp INT NOT NULL
        - cant DECIMAL(10,3) DEFAULT 0
        - data DATE

6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
Pretul de iesire va fi pretul din acel moment;  

9. Creati doua metode noi, diferite de cele facute la clasa, testatile si asigurativa ca functioneaza cu succes;


""" #
import pygal
import smtplib
import re
from datetime import datetime
from prettytable import PrettyTable
from tkinter import *
from tkinter import ttk
import mysql.connector


class Stoc:

    lista_prod = []
    lista_intrari = []
    lista_iesiri = []


    def __init__(self, denp, categ, um = 'kg', sold = 0):
        self.denp = denp
        self.categ = categ
        self.um = um
        self.sold = sold
        self.dict_op = {}
        self.lista_prod.append(denp)

    def genereaza_cheia(self):
        if self.dict_op:
           c = max(self.dict_op.keys()) + 1
        else:
            c = 1
        return c

    def intrari(self, cant, data = str ( datetime.now ( ).strftime ( '%Y%m%d' ) )):
        cheie = self.genereaza_cheia()
        self.dict_op[cheie] = [data, cant, 0]
        self.sold += cant
        self.lista_intrari.append(cant)

    def iesiri(self, cant, data = str ( datetime.now ( ).strftime ( '%Y%m%d' ) )):
        cheie = self.genereaza_cheia()
        self.dict_op[cheie] = [data, 0, cant]
        self.sold -= cant
        self.lista_iesiri.append(cant)

    def fisap(self):
        print('Fisa produsului {0}, {1}'.format(self.denp, self.um))
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']
        for k, v in self.dict_op.items():
            listeaza.add_row([k, v[0], v[1], v[2]])
        listeaza.add_row(['------','----------','---------','--------'])
        listeaza.add_row(['Sold', 'final', self.denp, self.sold])
        print(listeaza)

    def produse(self):
        for i in self.lista_prod:
            print(i)
            print(i.fisap)


    # Cerinta 1

    def proiectie_grafica(self):
        bar_chart = pygal.Bar (x_title = 'Perioada de timp',y_title = 'Cantitate', title_font_size = 30)
        bar_chart.title = 'Proiectie grafica pentru ' + self.denp
        date = []
        intrari = []
        iesiri = []
        for k,v in self.dict_op.items():
            date.append(v[0])
            intrari.append(v[1])
            iesiri.append(v[2])
        bar_chart.x_labels = date
        bar_chart.add('Intrari',intrari)
        bar_chart.add('Iesiri',iesiri)
        bar_chart.render()
        bar_chart.render_to_file('grafic.svg')  # salvare fisier grafic

    # Cerinta 2
    # avertizam cand stocul este mai mic decat limita minima predefinita per produs
    # limita variabila, am setat valoare default de 100

    def avertizare(self, limita=100):
        self.limita = limita
        if self.sold < limita:
            expeditor = 'mimidomer@gmail.com'
            destinatar = 'mimimm1@yahoo.com'

            username = 'mimidomer@gmail.com'
            parola = 'parolaproiect'

            mesaj = "Mesaj de avertizare: Stocul este mai mic decat limita"
            try:
                smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                smtpObj.starttls()
                smtpObj.login(username, parola)
                smtpObj.sendmail(expeditor, destinatar, mesaj)
                print('Mesaj expediat cu succes!')
            except:
                print('Mesajul nu a putut fi expediat!')
            finally:
                smtpObj.close()
        else:
            print('Stocul este in regula')

    # Cerinta 3

    def mail(self):

        expeditor = 'expeditor@gmail.com'
        destinatar = 'destinatar@yahoo.com'

        username = 'expeditor'
        parola = '12345'

        mesaj = "From: From Person <expeditor@gmail.com>"  \
        + "To: To Person <destinatar@yahoo.com>" \
        + "Subject: Detalii produs" \
        + "Denumire produs: " + str(self.denp) \
        + "Sold final: " + str(self.sold)

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(username, parola)
            smtpObj.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')
        finally:
            smtpObj.close()


    # Cerinta 4
    # Folosing regex:
    # caut un produs
    # sau caut o tranzactie

    def cautare(self):
        intrari = ""
        iesiri = ""
        optiune = int(input("""Introduceti :
             1 pentru cautare produs
             2 pentru cautare tranzactie"""))

        # cautam produsul
        if optiune == 1:
            produs = str(input('Introduceti numele produsului: '))
            for element in self.lista_prod:
                 m = re.match(produs, element)
            if m:
               print('Produsul a fost gasit!')

            else:
               print('Produsul nu a fost gasit!')

        # cautam tranzactia
        else:
            tranzactie = str(input('Introduceti tranzactia cautata: Intrari/Iesiri: '))
            val = input('Introduceti valoarea tranzactiei: ')
            for k,v in self.dict_op.items():
               intrari += str(v[1])
               iesiri += str(v[2])
            if tranzactie == 'Intrari':
                match_intrari = re.match(val,intrari)
                if match_intrari:
                  print(f'Tranzactia {tranzactie} cu valoarea {val} a fost gasita!')
                else:
                   print(f'Tranzactia {tranzactie} cu valoarea {val} nu a fost gasita!')
            else:
                match_iesiri = re.match(val,iesiri)
                if match_iesiri:
                    print(f'Tranzactia {tranzactie} cu valoarea {val} a fost gasita!')
                else:
                    print(f'Tranzactia {tranzactie} cu valoarea {val} nu a fost gasita!')


    # Cerinta 5 - SQL


    def sql(self):

        # Credentiale conectare
        host = "127.0.0.1"  # 'localhost'
        passwd = "root"
        port = 3306  # normal portul e 3306. Daca e diferit trebuie mentionat acela
        user = "root"
        dbname = "mydb"

        # Creare obiect conectare
        db = mysql.connector.connect(host=host, port=port, user=user, passwd=passwd, db=dbname)

        # Creare cursor
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS Categoria")
        cursor.execute("CREATE TABLE Categoria(idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY , denc VARCHAR(25))")
        cursor.execute("DROP TABLE IF EXISTS Produs")
        cursor.execute("CREATE TABLE Produs(idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY , idc INT NOT NULL, denp VARCHAR(25), pret DECIMAL(8,2) DEFAULT 0)")
        cursor.execute("DROP TABLE IF EXISTS Operatiuni")
        cursor.execute("CREATE TABLE Operatiuni(ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY , idp INT NOT NULL, cant DECIMAL(10,3) DEFAULT 0, data DATE)")



        # Cerinta 9
    # Prima metoda: sterge un produs introdus de utilizator din lista de produse

    def sterge_produs(self):
        produs = str(input('Ce produs doriti sa stergeti?'))
        if produs in self.lista_prod:
            self.lista_prod.remove(produs)
            print(f'Produsul cu numele {produs} a fost sters!')
        else:
            print(f'Produsul cu numele {produs} nu a fost gasit!')


    # A doua metoda : GUI

class MyGUI(Stoc):

    def __init__(self):

        self.window = Tk() # Am creat instanta
        self.window.title("Stoc Graphical User Interface")
        self.window.geometry('350x200')

        self.tab_control = ttk.Notebook(self.window)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Lista de Produse')


        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Total Intrari')

        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text='Total Iesiri')


        self.tab_control.pack(expand=1, fill="both")

        elem = "\n".join(self.lista_prod)
        self.lbl1 = Label(self.tab1, text=elem)
        self.lbl1.config(wraplength=110)  # modificare latime in pixeli
        self.lbl1.config(justify=CENTER)
        self.lbl1.config(foreground='black', background='pink')
        self.lbl1.config(font=('Times New Roman', 18, 'bold'))

        self.lbl1.grid(column=0, row=0)

        total_intrari = sum(self.lista_intrari)
        self.lbl2 = Label(self.tab2, text= total_intrari)
        self.lbl2.config(wraplength=110)  # modificare latime in pixeli
        self.lbl2.config(justify=CENTER)
        self.lbl2.config(foreground='black', background='yellow')
        self.lbl2.config(font=('Times New Roman', 18, 'bold'))

        self.lbl2.grid(column=0, row=0)

        total_iesiri = sum(self.lista_iesiri)
        self.lbl3 = Label(self.tab3, text= total_iesiri)
        self.lbl3.config(wraplength=110)  # modificare latime in pixeli
        self.lbl3.config(justify=CENTER)
        self.lbl3.config(foreground='black', background='green')
        self.lbl3.config(font=('Times New Roman', 18, 'bold'))

        self.lbl3.grid(column=0, row=0)

        self.window.mainloop()





mere = Stoc('mere','fructe')

mere.intrari(1000, '20200925')
mere.iesiri(765,'20201001')
# mere.intrari(300)
# mere.iesiri(20)

mere.fisap()
mere.proiectie_grafica()
mere.avertizare(250)
mere.mail()
mere.cautare()
mere.sterge_produs()
mere.sql()


struguri = Stoc('struguri','fructe')
struguri.intrari(3000)
struguri.iesiri(2000)
struguri.fisap()
struguri.proiectie_grafica()
struguri.avertizare(200)
struguri.mail()
struguri.cautare()
struguri.sterge_produs()


mure = Stoc('mure','fructe')
mure.intrari(150)
mure.iesiri(20)


castraveti = Stoc('castraveti','legume')
castraveti.intrari(600)
castraveti.iesiri(500)


banane = Stoc('banane','fructe')
banane.intrari(4000, '20200925')
banane.iesiri(3500,'20200925')


gui = MyGUI()

