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
WIDTH = 100
HEIGHT = 100
NUMBER_AGENTS = 10
ROUNDS = 10
FOOD_PERCENTAGE_BEGINNING = 1
ADDITIONAL_FOOD_PERCENTAGE = 0.5
SICKNESS_DURATION = ROUNDS // 10


# Globaler Counter
agents_counter = NUMBER_AGENTS

FOOD = {
    "1": {'Energy': 5, 'consume_time': 3, 'disease_risk': 0.0},  
    "2": {'Energy': 10, 'consume_time': 6, 'disease_risk': 0.0},
    "3": {'Energy': 15, 'consume_time': 9, 'disease_risk': 0.0},
    "5": {'Energy': 20, 'consume_time': 12, 'disease_risk': 0.},
    "4": {'Energy': 5, 'consume_time': 3, 'disease_risk': 0.0},
    "6": {'Energy': 10, 'consume_time': 6, 'disease_risk': 0.0},
    "7": {'Energy': 15, 'consume_time': 3, 'disease_risk': 0.0}   
}
FOOD_KEYS = list(FOOD.keys())

# Genpool
## evtl. Gene mit Wahrscheinlichkeiten, zb. Mut 
GENPOOL = {
    "Genes": {
        "Kondition": (1, 3),
        "Visibilityrange": (1, 3),
        "Tribe": (1, 3),
        "Resistance": (1, 5)
    }
}

class Agent:
    def __init__(self, number, sick = 0, birth):
        global agents_counter
        self.sickness_counter = 0
        self.number = number
        self.energy = START_ENERGY
        self.genetic = {}
        self.genedistribution()
        self.position = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
        self.reproduction_counter = 0
        self.consume_counter = 0
        self.sick = False
        self.sickness_duration = 0
        self.previous_kondition = None
        self.birth = birth
        self.lifespan = 0

    def genedistribution(self):
        #simulieren des Genverteilung aus dem festgelegten Dictionarie 'GENPOOL'
            for gen, bereich in GENPOOL["Genes"].items():
                # Ganzzahliger Wert für jedes Gen innerhalb der definierten Grenzen
                self.genetic[gen] = random.randint(*bereich)
                
    def consuming_food(self, food_dict):
        food = food_dict
        risk = food["disease_risk"]
        if random.random() < risk * (1 - self.genetic["Resistance"] / 5.0):
            self.sick = True
            self.sickness_duration = SICKNESS_DURATION
            self.sickness_counter += 1
            self.previous_kondition = self.genetic['Kondition']
            self.genetic["Kondition"] = 1
        self.energy += food["Energy"]
        self.consume_counter += 1

    def move(self, board):
        if self.energy > ENERGYCOSTS_MOVEMENT:
            if self.sick is True:
                self.check_for_sickness()
            
            else:
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

    def check_for_sickness(self):
        if self.sick:
            self.sickness_duration -= 1
            if self.sickness_duration <= 0:
                self.sick = False
                self.genetic["Kondition"] = self.previous_kondition

    def search_food(self, board):
        visibilityrange = self.genetic["Visibilityrange"]
        for dx in range(-visibilityrange, visibilityrange + 1):
            for dy in range(-visibilityrange, visibilityrange + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT and board.food[x][y] is not None:
                    food_dict = board.food[x][y]  # Schlüssel des Nahrungstyps
                    self.consuming_food(food_dict)  # Aufrufen von consuming_food mit dem Schlüssel
                    board.food[x][y] = None  # Entfernen der Nahrung von den Koordinaten
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
        self.food = np.full((width, height), None)
        self.world = np.zeros((width, height))

    def add_agent(self, agents_to_add):
        self.agents_list.append(agents_to_add)

    def place_food(self, prozent):
        amount_fields = int(self.width * self.height * prozent)
        for _ in range(amount_fields):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            food_type = random.choice(FOOD_KEYS)
            food_dict = FOOD[food_type]
            # Speichern des Nahrungstyps und der zugehörigen Werte direkt im food-Array
            self.food[x][y] = food_dict
    
        
    def remove_agents(self, agent):
        #removing the agents in the list 'lebewesen'
        self.agents_list.remove(agent)

class Game:
    def __init__(self, saving = False):
        self.saving = saving
        self.board = Board(WIDTH, HEIGHT)
        for i in range(1, NUMBER_AGENTS + 1):
            self.board.add_agent(Agent(i, birth = 0))
        self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
        
        
            
    def run(self):
        
        for round in range(ROUNDS):
            
            #ending the simulation in case there are no agents left
            if len(self.board.agents_list) == 0:
                print("--------------------------")
                print("\nall agents deceased\n")
                print("--------------------------")
                
                break
            if round % 10 == 0:
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                print(self.board.food)

            for agent in self.board.agents_list:
                agent.lifespan += 1
                
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
            writer.writerow(['Number', 'Tribe', 'Condition', 'Visibility Range', 'Reproduction Counter', 'Consume Counter', 'Position', 'Lifespan'])
            for agent in self.board.agents_list:
                writer.writerow([
                    agent.number, 
                    agent.genetic['Tribe'], 
                    agent.genetic['Kondition'], 
                    agent.genetic['Visibilityrange'], 
                    agent.reproduction_counter,
                    agent.consume_counter, 
                    agent.position,
                    agent.lifespan
                ])

                
    
# Counter einfügen wie oft sich ein Agents fortgepflanzt hat 
# Stammesangehörigkeit ausbessern: Aktuell Tupel für Stamm des Kindes

if __name__ == "__main__":
    start = time.time()
    game = Game(saving=True)
    #game = Game()
    game.run()
    script_time = np.round(time.time() - start, 2)
    print(script_time)