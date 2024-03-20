import tkinter as tk
import Symbols as sym
from tkinter import scrolledtext
from tk_html_widgets import HTMLText

class RaOptimize:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.contentFrame = tk.Frame(self.frame, width=700, height=600, borderwidth=1)
        self.contentFrame.grid(row=0, column=1, padx=10, pady=2)
        self.contentFrame.columnconfigure(2, weight=3)
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.grid_propagate(0)

        heading = tk.Label(self.contentFrame, text="Relačná algebra / Optimalizácia dopytu", width=50, height=3, font=("Arial", 10))
        heading.grid(row=1, column=2, padx=10, pady=2)

        self.entry = scrolledtext.ScrolledText(self.contentFrame, width=50, height=5, font=("Arial", 10))
        self.entry.grid(row=2, column=2, padx=10, pady=2, ipady=3)

        trBtn = tk.Button(self.contentFrame, text="Optimalizuj", command=self.translate)
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

        headingRa = tk.Label(self.contentFrame, text="Optimalizovaný Dopyt")
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
        self.entry.insert(tk.END, symbol+" ")

    def translate(self):
        self.optimizeRa()

    def optimizeRa(self):
        oldOgText = self.entry.get("1.0", tk.END)
        ogText = oldOgText.strip()  # vymazanie \n zo stringu
        trList = ogText.split(" ")
        if trList[-1] == ")":
            trList[-1] = "))"
        trText = ""
        trCopyText = ""
        tables = self.findTables(trList)
        join = self.findJoin(trList)
        i = 0
        for x in tables:
            pom = self.findSelect(trList, x)
            pom2 = self.findCondition(trList, x)
            if pom != None and pom2 == None:
                trText += sym.TEXT + "( " + sym.PROJECTION + " " + sym.KONIEC + sym.PREDIKAT + pom + sym.KONIEC
                trCopyText += "( " + sym.PROJECTION + " " + pom
            if pom == None and pom2 != None:
                trText += sym.TEXT + "( " + sym.SELECTION + " " + sym.KONIEC + sym.PREDIKAT + pom2 + sym.KONIEC
                trCopyText += "( " + sym.SELECTION + " " + pom2
            if pom != None and pom2 != None:
                trText += sym.TEXT + "( " + sym.PROJECTION + " " + sym.KONIEC + sym.PREDIKAT + pom + sym.KONIEC + \
                          sym.TEXT + "( " + sym.SELECTION + " " + sym.KONIEC + sym.PREDIKAT + pom2 + sym.KONIEC
                trCopyText += "( " + sym.PROJECTION + " " + pom + "( " + sym.SELECTION + " " + pom2

            if pom != None and pom2 != None:
                trText += sym.TEXT + "( " + x + " )" + " )) " + sym.KONIEC
                trCopyText += "( " + x + " )" + " )) "
            else:
                trText += sym.TEXT + "( " + x + " )) " + sym.KONIEC
                trCopyText += "( " + x + " )) "

            if i < len(tables)-1:
                trText += join[0][i]
                trCopyText += join[1][i]
                i += 1

        self.htmlText.set_html(trText)
        self.textRa.config(state=tk.NORMAL)
        if (str(self.textRa.get(0.0, tk.END)).isspace()):
            self.textRa.insert(0.0, trCopyText)
        self.textRa.config(state=tk.DISABLED)


    def findTables(self, text):
        tables = []
        for i in range(0, len(text)):
            if (text[i] == sym.JOIN or text[i] == sym.LEFTJOIN or text[i] == sym.RIGHTJOIN or text[i] == sym.FULLJOIN) or text[i] == "))":
                tables.append(text[i-1])
            if text[i] == "))":
                break
        return tables

    def findSelect(self, text, table):
        pom = ""
        for i in range(0, len(text)):
            if text[i] == "(":
                break
            if text[i].find(table, 0, len(table)) >= 0:
                pom += text[i] + " "
                pass
        if pom == "":
            pom = None
            return pom
        else:
            return pom

    def findCondition(self, text, table):
        pom = ""
        for j in range(0, len(text)):
            if text[j-1] == sym.SELECTION:
                for i in range (j, len(text)):
                    if text[i] == "(":
                        break
                    if text[i].find(table) >= 0 and (text[i+1] == "=" or text[i+1] == ">" or text[i+1] == "<" or text[i+1] == ">=" or text[i+1] == "<="):
                        pom += text[i] + " " + text[i+1] + " " + text[i+2] + " "
                        if text[i+3] == "AND" and text[i+4].find(table) >= 0:
                            pom += "AND "
                        elif text[i+3] == "OR" and text[i+4].find(table) >= 0:
                            pom += "OR "
                    #podmienka pre funkcie napriklad MIN(osoba.vek)
                    elif text[i].find(table) >= 0 and (text[i+1] != "=" or text[i] != ">" or text[i] != "<" or text[i] != ">=" or text[i] != "<="):
                        pom += text[i] + " "
                        if text[i + 1] == "AND" and text[i + 2].find(table) >= 0:
                            pom += "AND "
                        elif text[i + 1] == "OR" and text[i + 2].find(table) >= 0:
                            pom += "OR "
                break
        if pom == "":
            pom = None
            return pom
        else:
            return pom

    def findJoin(self, text):
        join = []
        joinCopy = []
        pom = ""
        pomCopy = ""
        for j in range(0, len(text)):
            if text[j-2] == "(" and (text[j] == sym.JOIN or text[j] == sym.LEFTJOIN or text[j] == sym.RIGHTJOIN or text[j] == sym.FULLJOIN):
                for i in range(j, len(text)):
                    if text[i] == sym.JOIN or text[i] == sym.LEFTJOIN or text[i] == sym.RIGHTJOIN or text[i] == sym.FULLJOIN:
                        pom += sym.TEXT + text[i] + sym.KONIEC + " " + sym.PREDIKAT + text[i+1] + " = " + \
                               text[i+3] + " " + sym.KONIEC
                        join.append(pom)
                        pom = ""
                        pomCopy += text[i] + " " + text[i+1] + " = " + text[i+3] + " "
                        joinCopy.append(pomCopy)
                        pomCopy = ""

                break
        return join, joinCopy