import numpy as np
import random
from Agent import position 
# Platzhalter, wo die Position der Agents an das Board weitergegeben wird
from Food import position
# Platzhalter, wo die Position des Foods an das Board weitergegeben wird

Population_Size = 10
#Hilft mir beim überlegen mir das erstmal mit ner festen ANzahl Agenten vorzustellen

class Grid():
    #Initialisieren des Boards
    def __init__(self, size):
        self.size = size
        self.grid = np.zeroes((size, size), dtype=int) 
        self.agents = [Agent(random.randint(0, size - 1), random.randint(0, size - 1), Genome([random.choice([0, 1]) for i in range(10)])) for i in range(Population_Size)]
        
        
    #Anzeigen des 2D Grid
    def display(self):
        for row in self.grid:
            row_str = ""
            for cell in row:
                if cell == 0:
                    row_str += "0 "
                    #display of an empty Space in array
                else:
                    row_str += "A "
                    #display of an Agent in array
                #Hier könnten auch dann noch mit elif unterscheidungen über Darstellung von z.B food in grid gemacht werden
            print(row_str.strip())
       

    # Aufrufen der Location der versch. Akteure
    # gleiches für food
    def get_location(self):
        agent_location = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] != 0:
                    agent_location.append((i, j))
        return agent_location
    
    # Food wäre im gleichen Stil, wenn aber mehr als 0 und A als Unterscheidung im Grid Abänderung von '!= 0' in '== A' wahrscheinlich zur genauen Zuordnung

    # Wie viele Akteure sind gerade auf dem Board dargestellt?
    # gleiches für food
    def population_count(self):
        return len(self.agents)

    # Aktualisieren Akteure/Location nach jeder Runde/"Generation"
    # per iter .csv Daten erfassen mit live Darstellung und Daten per life_cycle zum Abrufen & Visualisieren?
    def update(self):
        for agent in self.agents:
            agent.update(self)

    # das wäre unter der Annahme, dass in der Class Agents eine Methode/Funktion ist, wo der Agent sich selber updatet ob er noch lebt oder nicht und dies an das Board weitergibt/vom Board aufrufbar wäre
    # def update(self, grid):
    #     # Agenten bewegen sich zufällig
    #     dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    #     self.move(dx, dy)

    #     # Agenten essen Nahrung, wenn vorhanden
    #     if grid.grid[self.x, self.y] == 1:
    #         self.eat()
    #         grid.grid[self.x, self.y] = 0  # Nahrung wurde aufgegessen

    #     # Agenten sterben, wenn ihre Energie auf 0 fällt
    #     if self.energy <= 0:
    #         grid.grid[self.x, self.y] = 0  # Zelle ist nun leer
    #         grid.agents.remove(self)  # Agent wird aus der Liste entfernt

    # Bsp. Mock-up von Chat GPT

        pass




