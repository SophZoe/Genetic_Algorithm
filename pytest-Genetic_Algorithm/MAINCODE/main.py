import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
# Konstanten
ENERGIEKOSTEN_BEWEGUNG = 1
ENERGIEKOSTEN_FORTPFLANZUNG = 5
START_ENERGIE = 10
BREITE = 1000
HÖHE = 1000
ANZAHL_LEBEWESEN = 50
RUNDEN = 1000
ENERGIE_NAHRUNG = 5
NAHRUNG_ANFANGS_PROZENT = 0.5
NAHRUNG_ZUSATZ_PROZENT = 0.05

# Globaler Counter für die Nummerierung der Lebewesen
lebewesen_counter = ANZAHL_LEBEWESEN

# Genpool
## evtl. Gene mit Wahrscheinlichkeiten, zb. Mut 
GENPOOL = {
    "Gene": {
        "Kondition": (1, 3),
        "Sichtweite": (1, 3),
        "Stamm": (1, 3)
    }
}

class Lebewesen:
    def __init__(self, nummer, geburt):
        global lebewesen_counter
        self.nummer = nummer
        self.energie = START_ENERGIE
        self.genetik = {}
        self.genverteilung()
        self.position = (random.randint(0, BREITE-1), random.randint(0, HÖHE-1))
        self.fortpflanzungs_counter = 0
        self.geburt = geburt
        self.lebensspanne = 0

    def genverteilung(self):
            for gen, bereich in GENPOOL["Gene"].items():
                # Ganzzahliger Wert für jedes Gen innerhalb der definierten Grenzen
                self.genetik[gen] = random.randint(*bereich)

    def bewegen(self, board):
        if self.energie > ENERGIEKOSTEN_BEWEGUNG:
            self.energie -= ENERGIEKOSTEN_BEWEGUNG
            neue_position = self.suche_nahrung(board)
            if neue_position:
                self.position = neue_position
            else:
                # Zufällige Bewegung: -1 oder 1, multipliziert mit der Kondition
                dx = random.choice([-1, 1]) * self.genetik['Kondition']
                dy = random.choice([-1, 1]) * self.genetik['Kondition']

                neue_x = max(0, min(BREITE - 1, self.position[0] + dx))
                neue_y = max(0, min(HÖHE - 1, self.position[1] + dy))
                self.position = (neue_x, neue_y)
        else:
            return "gestorben"

    def suche_nahrung(self, board):
        sichtweite = self.genetik["Sichtweite"]
        for dx in range(-sichtweite, sichtweite + 1):
            for dy in range(-sichtweite, sichtweite + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < BREITE and 0 <= y < HÖHE and board.nahrung[x][y]:
                    board.nahrung[x][y] = 0
                    self.energie += ENERGIE_NAHRUNG
                    return (x, y)
        return None


    def fortpflanzen(self, partner, board):
        global lebewesen_counter
        if self.energie > ENERGIEKOSTEN_FORTPFLANZUNG and self.position == partner.position:
            erfolgsrate = 1 if self.genetik["Stamm"] == partner.genetik["Stamm"] else 0.3
            if random.random() < erfolgsrate:
                lebewesen_counter += 1
                kind = Lebewesen(lebewesen_counter)
                kind.genverteilung_durch_vererbung(self, partner)
                self.energie -= ENERGIEKOSTEN_FORTPFLANZUNG
                self.fortpflanzungs_counter += 1
                partner.fortpflanzungs_counter += 1
                board.add_lebewesen(kind)

    def genverteilung_durch_vererbung(self, elternteil1, elternteil2):
        for gen in GENPOOL["Gene"]:
            if gen == "Stamm":
                self.genetik[gen] = (elternteil1.genetik[gen], elternteil2.genetik[gen])
            else:
                gewicht = random.uniform(0, 1)
                gen_wert = (gewicht * elternteil1.genetik[gen] + (1 - gewicht) * elternteil2.genetik[gen]) / 2
                self.genetik[gen] = int(round(gen_wert, 3))

class Board:
    def __init__(self, breite, höhe):
        self.breite = breite
        self.höhe = höhe
        self.lebewesen = []
        self.nahrung = np.zeros((breite, höhe))

    def add_lebewesen(self, lebewesen):
        self.lebewesen.append(lebewesen)

    def platziere_nahrung(self, prozent):
        anzahl_felder = int(self.breite * self.höhe * prozent)
        for _ in range(anzahl_felder):
            x, y = random.randint(0, self.breite - 1), random.randint(0, self.höhe - 1)
            self.nahrung[x][y] = ENERGIE_NAHRUNG

    def entferne_lebewesen(self, lebewesen):
        self.lebewesen.remove(lebewesen)

class Game:
    def __init__(self):
        self.board = Board(BREITE, HÖHE)
        for i in range(1, ANZAHL_LEBEWESEN + 1):
            self.board.add_lebewesen(Lebewesen(i))
        self.board.platziere_nahrung(NAHRUNG_ANFANGS_PROZENT)

    def run(self):
        for runde in range(RUNDEN):
            if runde % 10 == 0:
                self.board.platziere_nahrung(NAHRUNG_ZUSATZ_PROZENT)

            for lebewesen in self.board.lebewesen:
                lebewesen.lebensspanne += 1
                #Updated Lebensspanne über jede laufende Runde

            for lebewesen in self.board.lebewesen[:]:
                ergebnis = lebewesen.bewegen(self.board)
                if ergebnis == "gestorben":
                    self.board.entferne_lebewesen(lebewesen)
                else:
                    for anderer in self.board.lebewesen:
                        if lebewesen != anderer:
                            lebewesen.fortpflanzen(anderer, self.board)
            ### Mögliches Laufzeitproblem: Doppelte For-Schleife sorgt für Quadratische Laufzeit O(n2)
        self.speichere_daten()

    def speichere_daten(self):
        with open('lebewesen_daten.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nummer', 'Stamm', 'Kondition', 'Sichtweite', 'Fortpflanzungs-Counter', 'Lebensspanne'])
            for lebewesen in self.board.lebewesen:
                writer.writerow([lebewesen.nummer, lebewesen.genetik['Stamm'], lebewesen.genetik['Kondition'], lebewesen.genetik['Sichtweite'], lebewesen.fortpflanzungs_counter, lebewesen.lebensspanne])
# Counter einfügen wie oft sich ein Lebewesen fortgepflanzt hat 
# Stammesangehörigkeit ausbessern: Aktuell Tupel für Stamm des Kindes

start = time.time()

if __name__ == "__main__":
    game = Game()
    game.run()

end = time.time()

timee = end-start
print(timee)