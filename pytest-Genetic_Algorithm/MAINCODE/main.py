import random
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import time
from matplotlib.pyplot import imshow

# Konstanten
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 10
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 10
ROUNDS = 21
ENERGY_FOOD = 5
FOOD_PERCENTAGE_BEGINNING = 0.5
ADDITIONAL_FOOD_PERCENTAGE = 0.05

# Globaler Counter für die Nummerierung der Lebewesen
agents_counter = NUMBER_AGENTS

# Genpool
## evtl. Gene mit Wahrscheinlichkeiten, zb. Mut 
GENPOOL = {
    "Genes": {
        "Kondition": (1, 3),
        "Visibilityrange": (1, 3),
        "Tribe": (1, 3)
    }
}

class Agent:
    def __init__(self, number):
        global agents_counter
        self.number = number
        self.energy = START_ENERGY
        self.genetic = {}
        self.genedistribution()
        self.position = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
        self.reproduction_counter = 0

    def genedistribution(self):
        #simulieren des Genverteilung aus dem festgelegten Dictionarie 'GENPOOL'
            for gen, bereich in GENPOOL["Genes"].items():
                # Ganzzahliger Wert für jedes Gen innerhalb der definierten Grenzen
                self.genetic[gen] = random.randint(*bereich)
                

    def move(self, board):
        if self.energy > ENERGYCOSTS_MOVEMENT:
            self.energy -= ENERGYCOSTS_MOVEMENT
            new_position = self.search_food(board)
            if new_position:
                self.position = new_position
            else:
                # Zufällige Bewegung: -1 oder 1, multipliziert mit der Kondition
                dx = random.choice([-1, 1]) * self.genetic['Kondition']
                dy = random.choice([-1, 1]) * self.genetic['Kondition']

                new_x = max(0, min(WIDTH - 1, self.position[0] + dx))
                new_y = max(0, min(HEIGHT - 1, self.position[1] + dy))
                self.position = (new_x, new_y)
        else:
            return "deceased"

    def search_food(self, board):
        visibilityrange = self.genetic["Visibilityrange"]
        for dx in range(-visibilityrange, visibilityrange + 1):
            for dy in range(-visibilityrange, visibilityrange + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT and board.food[x][y]:
                    board.food[x][y] = 0
                    self.energy += ENERGY_FOOD
                    return (x, y)
        return None


    def reproduce(self, partner, board):
        global agents_counter
        if self.energy > ENERGYCOSTS_REPRODUCTION and self.position == partner.position:
            success_rate = 1 if self.genetic["Tribe"] == partner.genetic["Tribe"] else 0.3
            if random.random() < success_rate:
                agents_counter += 1
                kind = Agent(agents_counter)
                kind.genedistribution_thru_heredity(self, partner)
                self.energy -= ENERGYCOSTS_REPRODUCTION
                self.reproduction_counter += 1
                partner.reproduction_counter += 1
                board.add_agent(kind)

    def genedistribution_thru_heredity(self, parent1, parent2):
        for gen in GENPOOL["Genes"]:
            if gen == "Tribe":
                self.genetic[gen] = (parent1.genetic[gen], parent2.genetic[gen])
            else:
                gewicht = random.uniform(0, 1)
                gen_value = (gewicht * parent1.genetic[gen] + (1 - gewicht) * parent2.genetic[gen]) / 2
                self.genetic[gen] = int(round(gen_value, 3))

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents_list = []
        self.food = np.zeros((width, height))
        self.world = np.zeros((width, height))

    def add_agent(self, agents_to_add):
        self.agents_list.append(agents_to_add)

    def place_food(self, prozent):
        amount_fields = int(self.width * self.height * prozent)
        for _ in range(amount_fields):
            
            #random Koordinaten an dem die Nahrung pltziert werden soll
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            
            #platzieren der Nahrung
            self.food[x][y] = ENERGY_FOOD
    
        
    def remove_agents(self, agent):
        #removing the agents in the list 'lebewesen'
        self.agents_list.remove(agent)

class Game:
    def __init__(self, saving = False):
        self.saving = saving
        self.board = Board(WIDTH, HEIGHT)
        for i in range(1, NUMBER_AGENTS + 1):
            self.board.add_agent(Agent(i))
        self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
        
        
            
    def run(self):
        print(type(self.board))
        for round in range(ROUNDS):
            if round % 10 == 0:
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                
                
            for agent in self.board.agents_list[:]:
                #bewegt die agents
                result = agent.move(self.board)

                
                #schaut ob der agent deceased ist, wenn ja, dann entfernt er diesen
                if result == "deceased":
                    self.board.remove_agents(agent)

                #wenn agent noch lebt wird die fortpflanzung weitergeführt
                    #vergleicht Agent mit potentiellen partnern
                else:
                    for partner in self.board.agents_list:
                        if agent != partner:
                            agent.reproduce(partner, self.board)
            
            
        if self.saving is True:    ### Mögliches Laufzeitproblem: Doppelte For-Schleife sorgt für Quadratische Laufzeit O(n2)
            self.save_data()

        
    def save_data(self):
        # Generiere den Pfad für das "results" Verzeichnis im aktuellen Arbeitsverzeichnis
        current_working_directory = os.getcwd()
        result_dir = os.path.join(current_working_directory, 'results')
        csv_index = 0
        
        # Erstelle das Verzeichnis, wenn es nicht existiert
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # Erstelle den Dateinamen für die CSV-Datei
        filename = os.path.join(result_dir, f'agent_data_{csv_index}.csv')
        while os.path.exists(filename):
            csv_index += 1
            filename = os.path.join(result_dir, f'agent_data_{csv_index}.csv')
        
        # Schreibe die Agenten-Daten in die CSV-Datei
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Number', 'Tribe', 'Condition', 'Visibility Range', 'Reproduction Counter', 'Position'])
            for agent in self.board.agents_list:
                writer.writerow([
                    agent.number, 
                    agent.genetic['Tribe'], 
                    agent.genetic['Kondition'], 
                    agent.genetic['Visibilityrange'], 
                    agent.reproduction_counter, 
                    agent.position
                ])

                
    
# Counter einfügen wie oft sich ein Agents fortgepflanzt hat 
# Stammesangehörigkeit ausbessern: Aktuell Tupel für Stamm des Kindes

if __name__ == "__main__":
    start = time.time()
    #game = Game(saving=True)
    game = Game()
    game.run()
    timee = np.round(time.time() - start, 2)
    print(timee)