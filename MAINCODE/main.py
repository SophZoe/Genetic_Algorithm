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
START_ENERGY = 20
WIDTH = 100
HEIGHT = 100
NUMBER_AGENTS = 50
ROUNDS = 100
FOOD_PERCENTAGE_BEGINNING = 1
ADDITIONAL_FOOD_PERCENTAGE = 0.5
SICKNESS_DURATION = ROUNDS // 10


# Globaler Counter
agents_counter = NUMBER_AGENTS

FOOD = {
    "1": {'Energy': 5, 'consumption_time': 2, 'disease_risk': 0},  
    "2": {'Energy': 10, 'consumption_time': 6, 'disease_risk': 0},
    "3": {'Energy': 15, 'consumption_time': 6, 'disease_risk': 0},
    "5": {'Energy': 20, 'consumption_time': 8, 'disease_risk': 3},
    "4": {'Energy': 5, 'consumption_time': 2, 'disease_risk': 6},
    "6": {'Energy': 10, 'consumption_time': 4, 'disease_risk': 9},
    "7": {'Energy': 15, 'consumption_time': 6, 'disease_risk': 12}   
}
FOOD_KEYS = list(FOOD.keys())

# Genpool
## evtl. Gene mit Wahrscheinlichkeiten, zb. Mut 
GENPOOL = {
    "Genes": {
        "Kondition": (1, 3),
        "Visibilityrange": (1, 3),
        "Tribe": (1, 3),
        "Resistance": (1, 3),
        "Metabolism": (1, 3),
        "Intelligent": [True, False],  # Verwendung einer Liste statt eines Tupels, um Klarheit zu schaffen
        "Aggressive": [True, False]
    }
}

class Agent:
    def __init__(self, number, sick = 0):
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
        self.flee_counter = 0
        self.previous_kondition = None
        self.parent_A  = None
        self.parent_B = None
        self.consumption_time = 0
        self.covered_distance = 0
        self.expelled = 0

    def genedistribution(self):
        for gen, bereich in GENPOOL["Genes"].items():
            if isinstance(bereich[0], bool):  
                self.genetic[gen] = random.choice(bereich)  # Gen zuerst initialisieren
                if self.genetic["Intelligent"] == True:  # Überprüfung des gesetzten Wertes
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True
            else:
                self.genetic[gen] = random.randint(*bereich)

    def consuming_food(self, food_dict):
        food = food_dict
        self.consumption_time = food_dict["consumption_time"] // max(1, self.genetic['Metabolism'])
        self.last_consumed_food_energy = food_dict["Energy"]  # Store the energy value for later
        risk = food["disease_risk"]
        if self.genetic["Intelligent"] is False:
            if random.random() < risk * (1 - self.genetic["Resistance"] / 3):
                self.sick = True
                self.sickness_duration = SICKNESS_DURATION
                self.sickness_counter += 1
                self.previous_kondition = self.genetic['Kondition']
                self.genetic["Kondition"] = 1



    def move(self, board):

        if self.consumption_time > 0:
            self.consumption_time -= 1  # Decrement the consumption timer
            
            # If consumption has just finished, add the energy from the last consumed food
            if self.consumption_time == 0:
                self.energy += self.last_consumed_food_energy  # Add the stored energy
                self.consume_counter += 1  # Increment the consume counter
                self.last_consumed_food_energy = 0  # Reset the stored energy to 0 for the next consumption
        
        else:
            if self.energy > ENERGYCOSTS_MOVEMENT:
                if self.sick is True:
                    self.check_for_sickness()
                
                else:
                    if self.flee_counter > 0:  # Fluchtmodus
                        self.flee_counter -= 1  

                        # Zufällige Bewegung: -1 oder 1, multipliziert mit der Kondition
                        dx = random.choice([-1, 1]) * self.genetic['Kondition']
                        dy = random.choice([-1, 1]) * self.genetic['Kondition']
                        new_x = max(0, min(WIDTH - 1, self.position[0] + dx))
                        new_y = max(0, min(HEIGHT - 1, self.position[1] + dy))
                        self.position = (new_x, new_y)
                       
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
                self.covered_distance += 1
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
                    food_dict = board.food[x][y]
                    # Prüfen, ob sich aggressive Agents in der Nähe befinden
                    aggressive_agents_nearby = self.check_for_aggressive_agents(board, x, y)

                    if aggressive_agents_nearby:
                        if not self.genetic["Aggressive"]:
                            # Nicht-aggressives Lebewesen hört auf zu fressen und bewegt sich weg
                            self.consumption_time = 0  # Beende das Essen
                            self.move_away_from_aggressive(board, aggressive_agents_nearby)
                            self.expelled += 1
                            return None  # Gehe zum Nächsten Futter        

                    if self.genetic["Intelligent"] is True and food_dict["disease_risk"] == 0:
                        self.consuming_food(food_dict)  # Aufrufen von consuming_food mit dem Schlüssel
                        board.food[x][y] = None  # Entfernen der Nahrung von den Koordinaten
                        return (x, y)
                    else:
                        self.consuming_food(food_dict)  # Aufrufen von consuming_food mit dem Schlüssel
                        board.food[x][y] = None  # Entfernen der Nahrung von den Koordinaten
                        return (x, y)
        return None

    def check_for_aggressive_agents(self, board, x, y):
        aggressive_agents = []
        search_radius = 2
        for agent in board.agents_list:
            if agent is not self and agent.genetic["Aggressive"]:
                distance = max(abs(agent.position[0] - x), abs(agent.position[1] - y))
                if distance <= search_radius:
                    aggressive_agents.append(agent)
        return aggressive_agents

    def move_away_from_aggressive(self, board, aggressive_agents):
        self.flee_counter = 5  # Initialisieren des Fluchtszählers
        self.consumption_time = 0

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
                self.genetic[gen] = random.choice([parent1.genetic[gen], parent2.genetic[gen]])
                self.parent_A = parent1.number
                self.parent_B = parent2.number
            elif gen == "Intelligent":
                self.genetic[gen] == random.choice([parent1.genetic[gen], parent2.genetic[gen]])
            else:
                gewicht = random.uniform(0, 1)
                gen_value = (gewicht * parent1.genetic[gen] + (1 - gewicht) * parent2.genetic[gen]) / 2
                self.genetic[gen] = int(round(gen_value, 3))
                if self.genetic["Intelligent"] == True:  # Überprüfung des gesetzten Wertes
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True

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
            self.board.add_agent(Agent(i))
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
        current_working_directory = os.getcwd() + "/MAINCODE/"
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
            writer.writerow(['Number', ' Tribe', ' Condition', ' Visibility Range', ' Metabolism', ' Intelligent', ' Aggressive', ' Covered Distance', ' Reproduction Counter', ' Consume Counter', ' Sickness Counter' ,' Parent A', ' Parent B', ' Position', ' Expelled'])
            for agent in self.board.agents_list:
                writer.writerow([
                    agent.number, 
                    agent.genetic['Tribe'], 
                    agent.genetic['Kondition'], 
                    agent.genetic['Visibilityrange'], 
                    agent.genetic['Metabolism'],
                    agent.genetic['Intelligent'],
                    agent.genetic['Aggressive'],
                    agent.covered_distance, 
                    agent.reproduction_counter,
                    agent.consume_counter,
                    agent.sickness_counter,
                    agent.parent_A,
                    agent.parent_B,
                    agent.position,
                    agent.expelled
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
