import tkinter as tk
import Symbols as sym
from tkinter import scrolledtext

class RaFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.contentFrame = tk.Frame(self.frame, width=700, height=600, borderwidth=1)
        self.contentFrame.grid(row=0, column=1, padx=10, pady=2)
        self.contentFrame.columnconfigure(2, weight=3)
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.grid_propagate(0)

        heading = tk.Label(self.contentFrame, text="Relačná algebra", width=50, height=3, font=("Arial", 10))
        heading.grid(row=1, column=2, padx=10, pady=2)

        self.entry = scrolledtext.ScrolledText(self.contentFrame, width=50, height=5, font=("Arial", 10))
        self.entry.grid(row=2, column=2, padx=10, pady=2, ipady=3)

        trBtn = tk.Button(self.contentFrame, text="Preloz", command=self.translate)
        trBtn.grid(row=2, column=3, padx=10, pady=2)

        delBtn = tk.Button(self.contentFrame, text="Zmaž", command=self.delete, bg="red")
        delBtn.grid(row=2, column=4, padx=10, pady=2)

        self.symbolFrame = tk.Frame(self.contentFrame, borderwidth=1)
        self.symbolFrame.grid(row=3, column=2, padx=10, pady=2)

        symbolBtn1 = tk.Button(self.symbolFrame, text=sym.PROJECTION, width=4, height=3, command=lambda : self.addSymbol(sym.PROJECTION))
        symbolBtn1.grid(row=1, column=1, padx=10, pady=2)
        symbolBtn2 = tk.Button(self.symbolFrame, text=sym.SELECTION, width=4, height=3, command=lambda : self.addSymbol(sym.SELECTION))
        symbolBtn2.grid(row=1, column=2, padx=10, pady=2)
        symbolBtn3 = tk.Button(self.symbolFrame, text=sym.JOIN, width=4, height=3, command=lambda : self.addSymbol(sym.JOIN))
        symbolBtn3.grid(row=1, column=3, padx=10, pady=2)
        symbolBtn4 = tk.Button(self.symbolFrame, text=sym.LEFTJOIN, width=4, height=3, command=lambda: self.addSymbol(sym.LEFTJOIN))
        symbolBtn4.grid(row=1, column=4, padx=10, pady=2)
        symbolBtn5 = tk.Button(self.symbolFrame, text=sym.RIGHTJOIN, width=4, height=3, command=lambda: self.addSymbol(sym.RIGHTJOIN))
        symbolBtn5.grid(row=1, column=5, padx=10, pady=2)
        symbolBtn6 = tk.Button(self.symbolFrame, text=sym.FULLJOIN, width=4, height=3, command=lambda: self.addSymbol(sym.FULLJOIN))
        symbolBtn6.grid(row=1, column=6, padx=10, pady=2)

        headingSQL = tk.Label(self.contentFrame, text="SQL")
        headingSQL.grid(row=5, column=1, padx=10, pady=2)
        self.textSQL = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                            highlightbackground="#333", font=("Arial", 10))
        self.textSQL.config(state=tk.DISABLED)
        self.textSQL.grid(row=5, column=2, padx=10, pady=2)
        cpySqlBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textSQL.get(1.0, "end-1c")))
        cpySqlBtn.grid(row=5, column=3, padx=10, pady=2)

        headingRk = tk.Label(self.contentFrame, text="Relačný kalkulus")
        headingRk.grid(row=4, column=1, padx=10, pady=2)
        self.textRk = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                           highlightbackground="#333", font=("Arial", 10))
        self.textRk.config(state=tk.DISABLED)
        self.textRk.grid(row=4, column=2, padx=10, pady=2)
        cpyRkBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textRk.get(1.0, "end-1c")))
        cpyRkBtn.grid(row=4, column=3, padx=10, pady=2)

        self.premennaJoin = " inner "
        self.dictionaryJoin = {sym.JOIN: " inner ", sym.FULLJOIN: " full ", sym.RIGHTJOIN: " right ", sym.LEFTJOIN: " left "}

    def destroy(self):
        self.contentFrame.destroy()

    def delete(self):
        self.textSQL.config(state=tk.NORMAL)
        self.textSQL.delete(1.0, tk.END)
        self.textSQL.config(state=tk.DISABLED)

        self.textRk.config(state=tk.NORMAL)
        self.textRk.delete(1.0, tk.END)
        self.textRk.config(state=tk.DISABLED)

    def copy(self, cpText):
        self.root.clipboard_clear()
        self.root.clipboard_append(cpText)
        self.root.update()

    def addSymbol(self, symbol):
        self.entry.insert(tk.END, symbol+" ")

    def translate(self):
        self.translateRk()
        self.translateSQL()

    #funkcia spraví preklad z RA do RK
    def translateRk(self):
        ogText = self.entry.get("1.0", tk.END)  # zkopirovaný text z RA premennej
        trList = ogText.split(" ")  # rozdelenie textu podla medzier
        trText = "{ N |"
        tables = self.findTablesRK(trList)
        tabRK = self.tabRK(tables)
        tablesText = self.tablesRK(tabRK)
        join = self.joinRK(trList, tabRK)
        select = self.selectRK(trList, tabRK)
        condition = self.conditionRK(trList, tabRK)
        trText += tablesText + join + condition + select + ")}"

        self.textRk.config(state=tk.NORMAL)
        if (str(self.textRk.get(0.0, tk.END)).isspace()):
            self.textRk.insert(0.0, trText)
        self.textRk.config(state=tk.DISABLED)

    # funkcia najde z RA všetky tabulky
    def findTablesRK(self, text):
        pom = []
        for i in range(0, len(text)):
            if text[i - 1] == "(" and text[i] != sym.SELECTION:
                pom.append(text[i])
            if text[i - 4] == sym.JOIN or (text[i-4] == sym.LEFTJOIN or text[i-4] == sym.RIGHTJOIN or text[i-4] == sym.FULLJOIN):
                pom.append(text[i])
        return pom

    def compare(self, a, b):
        pom = ""
        for i, (x, y) in enumerate(zip(a, b)):  # prechádza po písmenkách a porovnáva
            if y != x:  # ak sa nerovnajú
                if i == 0:  # a ak index nie je na prvom písmenu (ak sa už prvé písmená nerovnajú)
                    break  # skončí
                pom = y  # prvé nerovnajúce sa písmeno si zapíše
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
            if i + 1 == poc:
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
                if text[i - 1] == sym.JOIN or (text[i-1] == sym.LEFTJOIN or text[i-1] == sym.RIGHTJOIN or text[i-1] == sym.FULLJOIN):
                    j = i
                    self.premennaJoin = self.dictionaryJoin.get(text[i - 1])
                    dlzkaPredikat = i + 3
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
                if predikat[i - 1] == "=":
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
            for i in range(0, len(predikat) - 1):
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
                        pom += "N." + pom2[1] + " = " + key[j] + "." + pom2[1] + " "
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
            if text[i - 1] == sym.SELECTION:
                for j in range(i, len(text)):
                    predikat += text[j] + " "
                    if text[j + 1] == "(":
                        break
        if predikat == "":
            return pom
        predikat = predikat.split(" ")
        if poc == 1:
            for i in range(0, len(predikat) - 1):
                if predikat[i] == "=" or predikat[i] == ">" or predikat[i] == "<":
                    pom += key[0] + "." + predikat[i - 1] + " " + predikat[i] + " " + predikat[i + 1] + " "
                if predikat[i] == "AND":
                    pom += sym.AND + " "
                if predikat[i] == "OR":
                    pom += sym.OR + " "
            pom += sym.AND + " "
            return pom
        else:
            for i in range(0, len(predikat) - 1):
                for j in range(0, poc):
                    if predikat[i].find(value[j]) >= 0:
                        pom2 = predikat[i].split(".")
                        pom2[1] = pom2[1].replace(")", "")
                        pom += key[j] + "." + pom2[1] + " " + predikat[i + 1] + " " + predikat[i + 2] + " "
                if predikat[i] == "AND":
                    pom += sym.AND + " "
                if predikat[i] == "OR":
                    pom += sym.OR
            pom += sym.AND + " "
            return pom

#prekladanie z RK do SQL
    def translateSQL(self):
        oldOgText = self.textRk.get("1.0", tk.END)
        ogText = oldOgText.strip()  # vymazanie \n zo stringu
        trList = ogText.split(" ")
        trText = ""
        tables = self.findTableSQL(trList)
        select = self.findSelectSQL(trList, tables)
        join = self.findJoinSQL(trList, tables)
        condition = self.findConditionSQL(trList, tables)
        trText += select + join + condition

        self.textSQL.config(state=tk.NORMAL)
        if (str(self.textSQL.get(0.0, tk.END)).isspace()):
            self.textSQL.insert(0.0, trText)
        self.textSQL.config(state=tk.DISABLED)

    #funkcia najde vsetky tabulky
    def findTableSQL(self, text):
        dicTables = {}                  #pouzivam dictionary pre vytvorenie parov napriklad {'O': 'osoba'}
        pom = None
        for i in range(0, len(text)):
            if text[i] == "(":
                break
            if text[i-1] == sym.SETMEMBERSHIP:    # O ∈ osoba zapíše ako {'O': 'osoba'}
                pom = {text[i-2]: text[i]}
                dicTables.update(pom)
        return dicTables

    # funkcia najde select
    def findSelectSQL(self, text, tables):
        pom = "select "
        pom2 = None                         #pomocna premenna pri rozdelovani do tabulky
        j = 0
        for i in range(0, len(text)):
            if text[i-1] == "(":
                j = i
        # ak je jedna tabulka nepise tabulku pred vyberom napriklad (O.meno) vypise len meno
        # pri dvoch a viac vypise aj nabulku napriklad (O.meno, M.nazov) vypise (osoba.meno, mesto.priezvisko)
        if len(tables.keys()) == 1:
            for i in range(j, len(text)):
                if text[i] == sym.AND or text[i] == sym.OR:
                    if text[i-3][0] == "N" and text[i-3][1] == ".":             #ak je napríklad N.meno = O.meno
                        pom2 = text[i-3].split(".")                             #pri jednej tabulke si zapíše len meno
                        pom += pom2[1] + " , "
                if text[i] == ")}":
                    if text[i-3][0] == "N" and text[i-3][1] == ".":
                        pom2 = text[i-3].split(".")
                        pom += pom2[1] + " "
            return pom
        else:
            for i in range(j, len(text)):
                if text[i] == sym.AND or text[i] == sym.OR:
                    if text[i-3][0] == "N" and text[i-3][1] == ".":
                        pom2 = text[i-1].split(".")                             #pri dvoch a viac tabulkach vyberie zo slovnika
                        pom += tables.get(pom2[0]) + "." + pom2[1] + " , "      #takze (ak O = osoba) N.meno = O.meno bude osoba.meno
                if text[i] == ")}":
                    if text[i-3][0] == "N" and text[i-3][1] == ".":
                        pom2 = text[i-1].split(".")
                        pom += tables.get(pom2[0]) + "." + pom2[1] + " "
            return pom

    # funkcia najde tabulku a spravi join pri viac ako jednej
    def findJoinSQL(self, text, tables):
        pom = "from "
        j = 0
        poc = len(tables.keys()) # premenna na pocet tabuliek
        x = 1 #pomocna premenna pri pocte tabuliek
        for i in range(0, len(text)):
            if text[i-1] == "(":
                j = i
        #ak je jedna tabulka vypise len tu tabulku
        if len(tables.keys()) == 1:
            pom += list(tables.values())[0]
            return pom
        else:
            pom += list(tables.values())[0]
            for i in range(j, len(text)):
                if text[i] == sym.AND and x < poc:              #kontrolujem počet tabuliek s x (2 tabulky sú oddelene jednym /\)
                    pom2 = text[i-3].split(".")                 #(3 tabulky su dvomi /\ )
                    pom3 = text[i-1].split(".")
                    pom += self.premennaJoin + "join "
                    pom += tables.get(pom3[0]) + " on " + tables.get(pom2[0]) + "." + pom2[1] + " = " + tables.get(pom3[0]) + "." + pom3[1]
                    x += 1
                    self.premennaJoin = " inner "
            return pom

    # funkcia najde podmienku v RK
    def findConditionSQL(self, text, tables):
        pom = " where "
        poc = len(tables.keys())
        x = 1
        j = 0
        y = 0
        for i in range(0, len(text)):       #najdem prvu zatvorku ulozim do premennej j
            if text[i - 1] == "(":
                j = i
        for i in range(j, len(text)):       #najdem kde konci zapis join pri viac tabulkach
            if text[i] == sym.AND:
                x += 1
                if x == poc:
                    y = i + 1
                    break
        if poc == 1:
            if text[j][0] == "N" and text[j][1] == ".":             # vráti prázdnu premmenu nenachádza sa žiadna podmienka
                pom = ""
            else:
                for i in range(j, len(text)):
                    if text[i][0] == "N" and text[i][1] == ".":         #pri jednej tabulke od j(prva zatvorka)
                        break
                    if text[i] == sym.AND or text[i] == sym.OR:
                        pom2 = text[i-3].split(".")
                        pom += pom2[1] + " " + text[i-2] + " " + text[i-1] + " "
                        if text[i] == sym.AND and (text[i+1][0] != "N" and text[i][1] != "."):
                            pom += "AND "
                        if text[i] == sym.OR:
                            pom += "OR "
            return pom
        else:
            if text[y][0] == "N" and text[y][1] == ".":
                pom = ""
            else:
                for i in range(y, len(text)):                               #pri dvoch idem od y (po skonceni zapisu join)
                    if text[i][0] == "N" and text[i][1] == ".":
                        break
                    if text[i] == sym.AND or text[i] == sym.OR:
                        pom2 = text[i-3].split(".")
                        pom += tables.get(pom2[0]) + "." + pom2[1] + " " + text[i-2] + " " + text[i-1] + " "
                    if text[i] == sym.AND and (text[i+1][0] != "N" and text[i][1] != "."):
                        pom += "AND "
                    if text[i] == sym.OR:
                        pom += "OR "
            return pom
