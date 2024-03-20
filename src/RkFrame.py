import tkinter as tk
import Symbols as sym
from tk_html_widgets import HTMLText
from tkinter import scrolledtext

class RkFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.contentFrame = tk.Frame(self.frame, width=700, height=600, borderwidth=1)
        self.contentFrame.grid(row=0, column=1, padx=10, pady=2)
        self.contentFrame.columnconfigure(2, weight=3)
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.grid_propagate(0)

        heading = tk.Label(self.contentFrame, text="Relačný kalkulus", width=50, height=3, font=("Arial", 10))
        heading.grid(row=1, column=2, padx=10, pady=2)

        self.entry = scrolledtext.ScrolledText(self.contentFrame, width=50, height=5, font=("Arial", 10))
        self.entry.grid(row=2, column=2, padx=10, pady=2, ipady=3)
        self.entry.insert(tk.END, "{ N | ")

        trBtn = tk.Button(self.contentFrame, text="Preloz", command=self.translate)
        trBtn.grid(row=2, column=3, padx=10, pady=2)

        delBtn = tk.Button(self.contentFrame, text="Zmaž", command=self.delete, bg="red")
        delBtn.grid(row=2, column=4, padx=10, pady=2)

        self.symbolFrame = tk.Frame(self.contentFrame, borderwidth=1)
        self.symbolFrame.grid(row=3, column=2, padx=10, pady=2)

        symbolBtn1 = tk.Button(self.symbolFrame, text=sym.EXISTS, width=4, height=3,
                               command=lambda : self.addSymbol(sym.EXISTS))
        symbolBtn1.grid(row=1, column=1, padx=10, pady=2)
        symbolBtn2 = tk.Button(self.symbolFrame, text=sym.SETMEMBERSHIP, width=4, height=3,
                               command=lambda : self.addSymbol(sym.SETMEMBERSHIP))
        symbolBtn2.grid(row=1, column=2, padx=10, pady=2)
        symbolBtn3 = tk.Button(self.symbolFrame, text="AND", width=4, height=3,
                               command=lambda: self.addSymbol(sym.AND))
        symbolBtn3.grid(row=1, column=3, padx=10, pady=2)
        symbolBtn4 = tk.Button(self.symbolFrame, text="OR", width=4, height=3,
                               command=lambda: self.addSymbol(sym.OR))
        symbolBtn4.grid(row=1, column=4, padx=10, pady=2)
        symbolBtn5 = tk.Button(self.symbolFrame, text=sym.RBRACKET, width=4, height=3,
                               command=lambda: self.addSymbol(sym.RBRACKET))
        symbolBtn5.grid(row=1, column=5, padx=10, pady=2)

        headingSQL = tk.Label(self.contentFrame, text="SQL")
        headingSQL.grid(row=4, column=1, padx=10, pady=2)
        self.textSQL = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                            highlightbackground="#333", font=("Arial", 10))
        self.textSQL.config(state=tk.DISABLED)
        self.textSQL.grid(row=4, column=2, padx=10, pady=2)
        cpySqlBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textSQL.get(1.0, "end-1c")))
        cpySqlBtn.grid(row=4, column=3, padx=10, pady=2)

        headingRa = tk.Label(self.contentFrame, text="Relačná algebra")
        headingRa.grid(row=5, column=1, padx=10, pady=2)
        self.textRa = tk.Text(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                           highlightbackground="#333", font=("Arial", 10))
        self.textRa.config(state=tk.DISABLED)
        cpyRaBtn = tk.Button(self.contentFrame, text="Copy", command=lambda: self.copy(self.textRa.get(1.0, "end-1c")))
        cpyRaBtn.grid(row=5, column=3, padx=10, pady=2)

        self.htmlText = HTMLText(self.contentFrame, height=10, takefocus=0, highlightthickness=1,
                                 highlightbackground="#333", font=("Arial", 10), background="white")
        self.htmlText.grid(row=5, column=2, padx=10, pady=2)
        self.htmlText.config(state=tk.DISABLED)

    def destroy(self):
        self.contentFrame.destroy()

    def delete(self):
        self.textSQL.config(state=tk.NORMAL)
        self.textSQL.delete(1.0, tk.END)
        self.textSQL.config(state=tk.DISABLED)

        self.htmlText.config(state=tk.NORMAL)
        self.htmlText.delete(1.0, tk.END)
        self.htmlText.config(state=tk.DISABLED)

        self.textRa.config(state=tk.NORMAL)
        self.textRa.delete(1.0, tk.END)
        self.textRa.config(state=tk.DISABLED)

    def copy(self, cpText):
        self.root.clipboard_clear()
        self.root.clipboard_append(cpText)
        self.root.update()

    def addSymbol(self, symbol):
        self.entry.insert(tk.END, symbol + " ")

    def translate(self):
        self.translateSQL()
        self.translateRa()

    #prekladanie z RK do SQL
    def translateSQL(self):
        oldOgText = self.entry.get("1.0", tk.END)
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
                    pom += " inner join "
                    pom += tables.get(pom3[0]) + " on " + tables.get(pom2[0]) + "." + pom2[1] + " = " + tables.get(pom3[0]) + "." + pom3[1]
                    x += 1
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

    # prekladanie z SQL do RA
    def translateRa(self):
        oldOgText = self.textSQL.get("1.0", tk.END)
        ogText = oldOgText.strip()  # vymazanie \n zo stringu
        trList = ogText.split(" ")
        trText = ""
        trCopyText = ""
        tableText = self.findTable(trList)
        selText = self.findSelect(trList)
        conText = self.findCondition(trList)
        if conText[0] is not None:
            trText = selText[0] + sym.TEXT + "(" + sym.KONIEC + conText[0] + tableText[0] + sym.TEXT + ")" + sym.KONIEC
            trCopyText = selText[1] + "(" + conText[1] + tableText[1] + ")"
        else:
            trText = selText[0] + tableText[0]
            trCopyText = selText[1] + tableText[1]

        self.htmlText.set_html(trText)
        self.textRa.config(state=tk.NORMAL)
        if (str(self.textRa.get(0.0, tk.END)).isspace()):
            self.textRa.insert(0.0, trCopyText)
        self.textRa.config(state=tk.DISABLED)

    # pomocna premenna pri preklade z SQL do RA, slúži na nájdenie Selectu
    def findSelect(self, text):
        pom = ""  # premenna pre zobrazenie na obrazovku
        pomCopy = ""  # premenna pre skopirovanie do schranky

        # prechadza zoznam, ked najde select zacne kopirovat kym nenajde from
        for i in range(0, len(text)):
            if text[i] == "select":
                pom += sym.TEXT + sym.PROJECTION + sym.KONIEC + sym.PREDIKAT
                pomCopy += sym.PROJECTION + " "

            elif text[i] == "from":
                break
            else:
                if text[i] != "*":
                    pom += text[i] + " "
                    pomCopy += text[i] + " "
        pom += sym.KONIEC
        return pom, pomCopy

    # pomocna premenna pri preklade z SQL do RA najde tabulku/tabulky
    def findTable(self, text):
        pom = sym.TEXT + "("
        pom2 = None
        pom2Copy = None
        pomCopy = "( "
        # prechadza zozman, ked najde from zapise tabulku
        for i in range(0, len(text)):
            if text[i - 1] == "from":
                pom += text[i] + " "
                pomCopy += text[i] + " "
            # ak najde inner join prida znak JOIN a kopiruje dalej predikat, ak najde dalsi join skopiruje tabulku
            # a kopiruje predikat
            if text[i - 1] == "join" and (text[i-2] == "inner" or text[i-2] == "right" or text[i-2] == "left"):
                pom += sym.TEXT + sym.JOIN + sym.KONIEC + sym.PREDIKAT
                pomCopy += sym.JOIN + " "
                for j in range(i + 2, len(text)):
                    # kopiruje predikat kym nenarazi na where alebo na iny join s dalsou tabulkou
                    if text[j] == "where" or text[j] == "inner" or text[j] == "join":
                        break
                    pom += text[j] + " "
                    pomCopy += text[j] + " "
                pom += sym.TEXT + text[i] + sym.KONIEC
                pomCopy += text[i] + " "

        pom += sym.TEXT + ")" + sym.KONIEC
        pomCopy += ")"
        return pom, pomCopy

    # pomocna premenna pri preklade z SQL do RA najde podmienku
    def findCondition(self, text):
        pom = None
        pomCopy = None
        # prechadza zoznam, ked najde where kopiruje do konca zoznamu
        for i in range(0, len(text)):
            if text[i - 1] == "where":
                pom = sym.TEXT + sym.SELECTION + sym.KONIEC + sym.PREDIKAT
                pomCopy = " " + sym.SELECTION + " "
                for j in range(i, len(text)):
                    pom += text[j] + " "
                    pomCopy += text[j] + " "
        if pom:
            pom += sym.KONIEC
        return pom, pomCopy
