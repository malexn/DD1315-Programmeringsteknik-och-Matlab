# -*- coding: utf-8 -*-

import random


class Cells:
    # Innehåller orden, slumpar dem och kopierar dem. Avgör när de ska visas.
    def __init__(self, word):
        self.word = word
        self.status = 0

    def hide_word(self):
        self.status = 0

    def show_word(self):
        self.status = 1

    def show_word_permanent(self):
        self.status = 2

    def __str__(self):
        return str(self.word)


class Gameboard:
    # Ska skapa spelplanen

    def __init__(self, rad, kolumn):
        self.line = rad
        self.column = kolumn
        self.thegameboard = []

    def read_file(self, antal):
        # läser in orden, shufflar dem och kopierar dem
        with open("words.txt", "r", encoding="utf-8") as words_file:
            words = random.sample([line.rstrip('\n') for line in words_file], antal)
            wordlist = []
            for word in words:  # för alla ord i words lägger den till en kopia av ordet
                wordlist.append(Cells(word))
                wordlist.append(Cells(word))
            random.shuffle(wordlist)  # shufflar så att orden hamnar på random platser
            return wordlist

    def fylla_planen(self):
        antal = int(int(self.line * self.column) / 2)  # Antalet ord som ska slumpas in i spelplanen
        self.thegameboard = Gameboard.read_file(self, antal)

    def draw_board(self):
        cell = 0
        y = 0
        while y < self.line:
            x = 0
            while x < self.column:
                if self.thegameboard[cell].status == 2 or self.thegameboard[cell].status == 1:
                    print(self.thegameboard[cell].word, end=" ")
                else:
                    print("---", end=" ")
                cell += 1
                x += 1
            print("\n")
            y += 1


class Memory(Gameboard, Cells):

    def __init__(self, line, column):
        super().__init__(line, column)
        self.line = line
        self.column = column
        self.sp = Gameboard(line, column)
        self.sp.fylla_planen()

    def collect_cell(self, x, y):
        if x > 1:
            return self.line * (x - 1) + (y - 1)
        else:
            return (x - 1) + (y - 1)

    def spela(self):
        matches = 0
        moves = 0
        points = 10
        while True:
            while True:
                try:
                    val1 = input("Välj koordinater för första draget. T.ex 1 1 " + '\n')
                    list1 = val1.split(' ')  # skapar en lista för x & y värden
                    x1 = int(list1[0])  # Första indexet i listan
                    y1 = int(list1[1])  # Andra indexet i listan
                except IndexError:
                    print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                except ValueError:
                    print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                else:
                    try:
                        if 0 > x1 or x1 > self.line or 0 > y1 or y1 > self.column:
                            print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                        else:
                            forsok1 = self.sp.thegameboard[self.collect_cell(x1, y1)]
                            forsok1.show_word()
                            self.sp.draw_board()
                            break
                    except IndexError:
                        print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
            while True:
                try:
                    val2 = input("Välj koordinater för andra draget. T.ex 1 1 " + '\n')
                    list2 = val2.split(' ')  # skapar en lista för x & y värden
                    x2 = int(list2[0])  # Första indexet i listan
                    y2 = int(list2[1])  # Andra indexet i listan
                except IndexError:
                    print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                except ValueError:
                    print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                else:
                    try:
                        if 0 > x2 or x2 > self.line or 0 > y2 or y2 > self.column:
                            print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')
                        else:
                            forsok2 = self.sp.thegameboard[self.collect_cell(x2, y2)]
                            forsok2.show_word()
                            self.sp.draw_board()
                            break
                    except IndexError:
                        print("*** Förstod inte riktigt dina koordinater, prova en gång till ***" + '\n')

            if forsok1.word == forsok2.word and x2-x1 == 0 and y2-y1 == 0:
                forsok1.hide_word()
                forsok2.hide_word()
                self.sp.draw_board()
                moves += 1
                points -= 1
                print("Det är samma kort! Försök igen." + '\n')
            elif forsok1.word != forsok2.word:
                forsok1.hide_word()
                forsok2.hide_word()
                moves += 1
                points -= 1
                print('Inte ett par. Hittade', forsok1.word, 'på (' + str(x1) + ',' + str(y1) + ') och', forsok2.word,
                    'på (' + str(x2) + ',' + str(y2) + ')' + '\n')
            else:
                forsok1.show_word_permanent()
                forsok2.show_word_permanent()
                matches += 1
                moves += 1
                points += 1
                print("SWEEET, du fick ett par!" + '\n')
                if matches == (self.line*self.column/2):
                    break
        self.scores = (moves*matches + points)
        print('Grattis! Du vann!' + '\n')
        print("Du har gjort ", moves, " antal försök." + '\n')
        print("Du fick ihop ", self.scores, "poäng." + '\n')
        self.save_highs()

    def save_highs(self):
        highscore = {}
        listofnames = []
        with open("highscore.txt", "r") as file:  # öppnar fil, loopar igenom den
            all_lines = file.readlines()
            for lines in all_lines:
                splitlines = lines.split(' ')
                highscore[splitlines[0]] = splitlines[1].strip('\n')
                listofnames.append(splitlines[0])
        name = input("Vad är ditt namn? " + '\n')
        highscore[name] = self.scores
        if name not in listofnames:  # om namnet inte finns med läggs den till
            listofnames.append(name)

        with open("highscore.txt", "w") as file:  # skriver till filen
            for names in listofnames:
                line = names + ' ' + str(highscore[names]) + '\n'
                file.write(line)
        file.close()
        print(highscore)


def main():
    print("\n\t--------------------\n\t      Välkommen\n\t        till\n\t       Memory\n\t--------------------")

    while True:
        while True:
            line = input("Välj antal rader. (siffra) " + '\n')
            if line.isdigit() and (2 <= int(line) <= 8):
                line = int(line)
                break
            else:
                print("*** Du måste välja mellan 2 och 8! Prova igen. ***" + '\n')
        while True:
            column = input("Välj antal kolumner " + '\n')
            if column.isdigit() and (2 <= int(column) <= 8):
                column = int(column)
                break
            else:
                print("*** Antal kolumner måste vara mellan 1 och 8! Prova igen. ***" + '\n')

        if line * column % 2 == 0:  # Ser till så att det blir ett jämnt antal platser
            break
        else:
            print("*** Antalet rader X kolumner måste vara jämnt. *** " + '\n')
    spel = Memory(line, column)
    spel.spela()

if __name__ == '__main__':
    main()
    input("\n\nPress the enter key to exit. " + '\n')