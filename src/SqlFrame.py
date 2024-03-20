import tkinter as tk
import Symbols as sym
from tk_html_widgets import HTMLText
from tkinter import scrolledtext

class SqlFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.contentFrame = tk.Frame(self.frame, width=700, height=600, borderwidth=1)
        self.contentFrame.grid(row=0, column=1, padx=10, pady=2)
        self.contentFrame.columnconfigure(2, weight=3)
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.grid_propagate(0)

        heading = tk.Label(self.contentFrame, text="SQL", width=50, height=3, font=("Arial", 10))
        heading.grid(row=1, column=2, padx=10, pady=2)

        self.entry = scrolledtext.ScrolledText(self.contentFrame, width=50, height=5, font=("Arial", 10))
        self.entry.grid(row=2, column=2, padx=10, pady=2, ipady=3)

        trBtn = tk.Button(self.contentFrame, text="Preloz", command=self.translate)
        trBtn.grid(row=2, column=3, padx=10, pady=2)

        delBtn = tk.Button(self.contentFrame, text="Zmaž", bg="red", command=self.delete)
        delBtn.grid(row=2, column=4, padx=10, pady=2)

        headingRa = tk.Label(self.contentFrame, text="Relačná algebra")
        headingRa.grid(row=4, column=1, padx=10, pady=2)
        self.textRa = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                           highlightbackground="#333", font=("Arial", 10))
        cpyRaBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textRa.get(1.0, "end-1c")))
        cpyRaBtn.grid(row=4, column=3, padx=10, pady=2)

        headingRk = tk.Label(self.contentFrame, text="Relačný kalkulus")
        headingRk.grid(row=5, column=1, padx=10, pady=2)
        self.textRk = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                           highlightbackground="#333", font=("Arial", 10))
        self.textRk.config(state=tk.DISABLED)
        self.textRk.grid(row=5, column=2, padx=10, pady=2)
        cpyRkBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textRk.get(1.0, "end-1c")))
        cpyRkBtn.grid(row=5, column=3, padx=10, pady=2)

        self.htmlText = HTMLText(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                           highlightbackground="#333", font=("Arial", 10), background="white")
        self.htmlText.grid(row=4, column=2, padx=10, pady=2)
        self.htmlText.config(state=tk.DISABLED)

    def destroy(self):
        self.contentFrame.destroy()

    # funkcia na zmazanie textu z okien RA a RK
    def delete(self):
        self.textRa.config(state=tk.NORMAL)
        self.textRa.delete(1.0, tk.END)
        self.textRa.config(state=tk.DISABLED)

        self.htmlText.config(state=tk.NORMAL)
        self.htmlText.delete(1.0, tk.END)
        self.htmlText.config(state=tk.DISABLED)

        self.textRk.config(state=tk.NORMAL)
        self.textRk.delete(1.0, tk.END)
        self.textRk.config(state=tk.DISABLED)

    # funkcia na skopírovanie textu z okien RA a RK do schránky
    def copy(self, cpText):
        self.root.clipboard_clear()
        self.root.clipboard_append(cpText)
        self.root.update()

    def translate(self):
        self.translateRa()
        self.translateRk()

    #prekladanie z SQL do RA
    def translateRa(self):
        oldOgText = self.entry.get("1.0", tk.END)   #original skopírovaný text
        ogText = oldOgText.strip()                  #vymazanie \n zo stringu
        trList = ogText.split(" ")                  #rozdelenie textu podla medzier (treba písať všade medzery)
        trText = ""
        trCopyText = ""
        tableText = self.findTable(trList)
        selText = self.findSelect(trList)
        conText = self.findCondition(trList)

        #ak je vo výraze podmienka
        if conText[0] is not None:
            trText = selText[0] + sym.TEXT+"("+sym.KONIEC + conText[0] + tableText[0] + sym.TEXT+")"+sym.KONIEC
            trCopyText = selText[1] + "(" + conText[1] + tableText[1] + ")"
        else:
            trText = selText[0] + tableText[0]                  #ak nie je vo výraze podmienka
            trCopyText = selText[1] + tableText[1]

        self.htmlText.set_html(trText)
        self.textRa.config(state=tk.NORMAL)
        if (str(self.textRa.get(0.0, tk.END)).isspace()):
            self.textRa.insert(0.0, trCopyText)
        self.textRa.config(state=tk.DISABLED)

    # pomocna premenna pri preklade z SQL do RA, slúži na nájdenie Selectu
    def findSelect(self, text):
        pom =""                                 #premenna pre zobrazenie na obrazovku
        pomCopy = ""                            #premenna pre skopirovanie do schranky
        for i in range(0, len(text)):
            if text[i] == "select":
                pom += sym.TEXT+sym.PROJECTION+sym.KONIEC+sym.PREDIKAT
                pomCopy += sym.PROJECTION + " "
            elif text[i] == "from":
                break
            else:
                if text[i] != "*":
                    pom += text[i]+" "
                    pomCopy += text[i]+" "
        pom += sym.KONIEC
        return pom, pomCopy

    #pomocna premenna pri preklade z SQL do RA najde tabulku/tabulky
    def findTable(self, text):
        pom = sym.TEXT + "("
        pom2 = None
        pom2Copy = None
        pomCopy = "( "
        #prechadza zozman, ked najde from zapise tabulku
        for i in range(0, len(text)):
            if text[i-1] == "from":
                pom += text[i] + " "
                pomCopy += text[i] + " "
            #ak najde inner join prida znak JOIN a kopiruje dalej predikat, ak najde dalsi join skopiruje tabulku
            #a kopiruje predikat
            if text[i-1] == "join":
                if text[i-2] == "inner":
                    pom += sym.TEXT + sym.JOIN + sym.KONIEC + sym.PREDIKAT
                    pomCopy += sym.JOIN + " "
                if text[i-2] == "left":
                    pom += sym.TEXT + sym.LEFTJOIN + sym.KONIEC + sym.PREDIKAT
                    pomCopy += sym.LEFTJOIN + " "
                if text[i-2] == "right":
                    pom += sym.TEXT + sym.RIGHTJOIN + sym.KONIEC + sym.PREDIKAT
                    pomCopy += sym.RIGHTJOIN + " "
                if text[i-2] == "full":
                    pom += sym.TEXT + sym.FULLJOIN + sym.KONIEC + sym.PREDIKAT
                    pomCopy += sym.FULLJOIN + " "
                for j in range(i+2, len(text)):
                    #kopiruje predikat kym nenarazi na where alebo na iny join s dalsou tabulkou
                    if text[j] == "where" or text[j] == "join" or text[j] == "inner" or text[j] == "right" or text[j] == "left" or text[j] == "full":
                        break
                    pom += text[j] + " "
                    pomCopy += text[j] + " "
                pom += sym.TEXT + text[i] + sym.KONIEC
                pomCopy += text[i] + " "

        pom += sym.TEXT + ")" + sym.KONIEC
        pomCopy += ")"
        return pom, pomCopy

    #pomocna premenna pri preklade z SQL do RA najde podmienku
    def findCondition(self, text):
        pom = None
        pomCopy = None
        for i in range(0, len(text)):
            if text[i-1] == "where":
                pom = sym.TEXT + sym.SELECTION + sym.KONIEC + sym.PREDIKAT
                pomCopy = " " + sym.SELECTION + " "
                for j in range(i, len(text)):
                    pom += text[j] + " "
                    pomCopy += text[j] + " "
        if pom:
            pom += sym.KONIEC
        return pom, pomCopy

    #funkcia pre preklad z RA do RK
    def translateRk(self):
        ogText = self.textRa.get("1.0", tk.END)         #zkopirovaný text z RA premennej
        trList = ogText.split(" ")                      #rozdelenie textu podla medzier
        trText = "{ N |"
        tables = self.findTablesRK(trList)
        tabRK = self.tabRK(tables)
        tablesText = self.tablesRK(tabRK)
        join = self.joinRK(trList, tabRK)
        select = self.selectRK(trList, tabRK)
        condition = self.conditionRK(trList, tabRK)
        trText += tablesText + join + condition + select +")}"

        self.textRk.config(state=tk.NORMAL)
        if (str(self.textRk.get(0.0, tk.END)).isspace()):
            self.textRk.insert(0.0, trText)
        self.textRk.config(state=tk.DISABLED)

    #funkcia najde z RA všetky tabulky
    def findTablesRK(self, text):
        pom = []
        for i in range(0, len(text)):
            if text[i-1] == "(" and text[i] != sym.SELECTION:
                pom.append(text[i])
            if text[i-4] == sym.JOIN or (text[i-4] == sym.LEFTJOIN or text[i-4] == sym.RIGHTJOIN or text[i-4] == sym.FULLJOIN):
                pom.append(text[i])
        return pom

    def compare(self, a, b):
        pom = ""
        for i, (x, y) in enumerate(zip(a,b)):           #prechádza po písmenkách a porovnáva
            if y != x:                                  #ak sa nerovnajú
                if i==0:                                #a ak index nie je na prvom písmenu (ak sa už prvé písmená nerovnajú)
                    break                               #skončí
                pom = y                                 #prvé nerovnajúce sa písmeno si zapíše
                break
        return pom

    def tabRK(self, arrayTables):
        tab = {}
        for i in range(0, len(arrayTables)):
            if i == 0:
                pom = {arrayTables[i][0].upper(): arrayTables[i]}
                tab.update(pom)
            if i + 1 < len(arrayTables) and arrayTables[i][0] == arrayTables[i + 1][0]:
                z = self.compare(arrayTables[i], arrayTables[i + 1])
                pom = {arrayTables[i + 1][0].upper() + z: arrayTables[i + 1]}
                tab.update(pom)
        poc = len(tab.keys())
        if poc < len(arrayTables):
            x = poc
            for i in range(x, len(arrayTables)):
                pom = {arrayTables[i][0].upper(): arrayTables[i]}
                tab.update(pom)
        return tab

    def tablesRK(self, tables):
        pom = ""
        poc = len(tables.keys())
        key = list(tables.keys())
        value = list(tables.values())
        for i in range(0, poc):
            pom += " ∃ " + key[i] + " ∈ " + value[i]
            if i+1 == poc:
                pom += " ("
            else:
                pom += " /\\"
        return pom

    def joinRK(self, text, tables):
        pom = " "
        poc = len(tables.keys())
        key = list(tables.keys())
        value = list(tables.values())
        if poc == 1:
            return pom
        else:
            predikat = ""
            j = 0
            dlzkaPredikat = 0
            for i in range(0, len(text)):
                if text[i-1] == sym.JOIN or (text[i-1] == sym.LEFTJOIN or text[i-1] == sym.RIGHTJOIN or text[i-1] == sym.FULLJOIN):
                    j = i
                    dlzkaPredikat = i+3
                    for x in range(j, dlzkaPredikat):
                        predikat += text[x] + " "
            predikat = predikat.split(" ")
            for i in range(0, len(predikat)):
                for j in range(0, poc):
                    if predikat[i].find(value[j], 0, len(value[j])) >= 0:
                        pom2 = predikat[i].split(".")
                        pom += key[j] + "." + pom2[1] + " "
                if predikat[i] == "=":
                    pom += "= "
                if predikat[i-1] == "=":
                    pom += "/\\ "
            return pom

    def selectRK(self, text, tables):
        pom = ""
        predikat = ""
        poc = len(tables.keys())
        key = list(tables.keys())
        value = list(tables.values())

        for i in range(0, len(text)):
            if text[i] != sym.PROJECTION:
                predikat += text[i] + " "
            if text[i + 1] == "(":
                break
        predikat = predikat.split(" ")
        if poc == 1:
            for i in range(0, len(predikat)-1):
                if predikat[i] != ",":
                    pom += "N." + predikat[i] + " = " + key[0] + "." + predikat[i] + " "
                else:
                    pom += "/\\ "
            return pom
        else:
            for i in range(0, len(predikat)):
                for j in range(0, poc):
                    if predikat[i].find(value[j]) >= 0:
                        pom2 = predikat[i].split(".")
                        pom2[1] = pom2[1].replace(")", "")
                        pom += "N."+pom2[1] + " = " + key[j] + "." + pom2[1] + " "
                if predikat[i] == ",":
                    pom += "/\\ "
            return pom

    def conditionRK(self, text, tables):
        pom = ""
        predikat = ""

        poc = len(tables.keys())
        key = list(tables.keys())
        value = list(tables.values())

        for i in range(0, len(text)):
            if text[i-1] == sym.SELECTION:
                for j in range(i, len(text)):
                    predikat += text[j] + " "
                    if text[j + 1] == "(":
                        break
        if predikat == "":
            return pom
        predikat = predikat.split(" ")
        if poc == 1:
            for i in range(0, len(predikat)-1):
                if predikat[i] == "=" or predikat[i] == ">" or predikat[i] == "<" or predikat[i] == "!=":
                    pom += key[0] + "." + predikat[i-1] + " " + predikat[i] + " " + predikat[i+1] + " "
                if predikat[i] == "AND":
                    pom += sym.AND + " "
                if predikat[i] == "OR":
                    pom += sym.OR + " "
            pom += sym.AND + " "
            return pom
        else:
            for i in range(0, len(predikat)-1):
                for j in range(0, poc):
                    if predikat[i].find(value[j]) >= 0:
                        pom2 = predikat[i].split(".")
                        pom2[1] = pom2[1].replace(")", "")
                        pom += key[j] + "." + pom2[1] + " " + predikat[i+1] + " " + predikat[i+2] + " "
                if predikat[i] == "AND":
                    pom += sym.AND + " "
                if predikat[i] == "OR":
                    pom += sym.OR + " "
            pom += sym.AND + " "
            return pom