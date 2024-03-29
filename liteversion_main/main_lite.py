# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 18:39:03 2024

@author: marko
"""
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
from matplotlib.pyplot import imshow
import numba

# Konstanten
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 5
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 1
ROUNDS = 400
ENERGY_FOOD = 5
FOOD_PERCENTAGE_BEGINNING = 1
ADDITIONAL_FOOD_PERCENTAGE = 0

# Globaler Counter für die Nummerierung der Lebewesen
agents_counter = NUMBER_AGENTS

# Genpool
## evtl. Gene mit Wahrscheinlichkeiten, zb. Mut 
GENPOOL = {
    "Genes": {
        "Kondition": (1, 3),
        "Visibilityrange": (2,2),
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
        closest_food = None
        food_key = 0
        visibilityrange = self.genetic["Visibilityrange"]
        for dx in range(-visibilityrange, visibilityrange + 1):
            for dy in range(-visibilityrange, visibilityrange + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT and board.food[x][y]:
                    closest_food = x, y
                    food_key = board.food[x][y]
                    board.food[x][y] = 0
                    self.energy += ENERGY_FOOD
                    print(f"key is {food_key}")
                    print(f"closest food coordinates are {closest_food}")

                    return closest_food, food_key


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
            
            
    def place_agents(self):
        #deleting the array so deceased agents will not be shown
        self.world = np.zeros_like(self.world)
        
        #placing agents in array
        for agent in self.agents_list:
            x, y = agent.position
            self.world[x][y] + 1
        
    def remove_agents(self, agent):
        #removing the agents in the list 'lebewesen'
        self.agents_list.remove(agent)

class Game:
    def __init__(self):
        self.board = Board(WIDTH, HEIGHT)
        for i in range(1, NUMBER_AGENTS + 1):
            self.board.add_agent(Agent(i))
        self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
        self.list_data = []
        
        
            
    def run(self):
        print("----------Round 0------------")
        #fillng the world with agents for the start
        self.board.place_agents()
        
        #visualizing the board
        self.visualize_board() 
        
        
        self.list_data = self.board.agents_list
        self.safe_data_beginning()
        for round in range(ROUNDS):
            #counter for Rounds
            print(f"\n------------Round {round+1}------------")  
            
            #ending the simulation in case there are no agents left
            if len(self.board.agents_list) == 0:
                print("--------------------------")
                print("\nall agents deceased\n")
                print("--------------------------")
                
                break 
            
            
            for agent in self.board.agents_list[:]:
                
                #moves the agents
                result = agent.move(self.board)
                """for agent in self.board.agents_list:
                    print(f"position: {agent.position}")"""
                
                #schaut ob der agent deceased ist, wenn ja, dann entfernt er diesen
                if result == "deceased":
                    self.board.remove_agents(agent)

                #wenn agent noch lebt wird die fortpflanzung weitergeführt
                    #vergleicht Agent mit potentiellen partnern
                else:
                    for partner in self.board.agents_list:
                        if agent != partner:
                            agent.reproduce(partner, self.board)
                
                
                
            
              
            #placing additional food and all agents in every round
            self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
            self.board.place_agents()
            
            #self.list_data.append(self.board.agents_list)
            
            #visualizing the board in every round
            self.visualize_board() 
            
            if round % 10 == 0:
                #placing additional food and all agents every 10 rounds
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                self.board.place_agents()
                
                #visualizing the board every 10 rounds
                self.visualize_board() 
                
                
                
               
            
        self.board.place_agents()  
        
        #visualizing after ending the simulation
        self.visualize_board()  
            ### Mögliches Laufzeitproblem: Doppelte For-Schleife sorgt für Quadratische Laufzeit O(n2)
            
        #saving data in csv
        self.safe_data_end()

    def safe_data_beginning(self):
        with open('agents_daten_beginning.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Number', 'Tribe', 'Kondition', 'Visibilityrange', 'Fortpflanzungs-Counter', 'Position'])
            for agent in self.list_data:
                writer.writerow([agent.number, agent.genetic['Tribe'], agent.genetic['Kondition'], agent.genetic['Visibilityrange'], agent.reproduction_counter, agent.position])
    def safe_data_end(self):
        with open('agents_daten_end.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Number', 'Tribe', 'Kondition', 'Visibilityrange', 'Fortpflanzungs-Counter', 'Position'])
            for agent in self.list_data:
                writer.writerow([agent.number, agent.genetic['Tribe'], agent.genetic['Kondition'], agent.genetic['Visibilityrange'], agent.reproduction_counter, agent.position])
  
    def visualize_board(self):
        #5 seconds pause between each time visualizing 
        #time.sleep(2)
        
        plt.rcParams["figure.figsize"] = [7.50, 4.5]
        plt.rcParams["figure.autolayout"] = True
        
        dx, dy = 0.05, 0.05
        x = np.arange(-3.0, 3.0, dx)
        y = np.arange(-3.0, 3.0, dy)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)
        
        fig = plt.figure(frameon=False)
        
        data1 = self.board.food
        plot1 = plt.imshow(data1, cmap="YlGn", interpolation='nearest', extent=extent)
        
        data2 = self.board.world
        plot2 = plt.imshow(data2, cmap="YlOrRd",alpha = .7, interpolation='gaussian', extent=extent)
        
        
        # set imshow outline to white
        for spine in plot2.axes.spines.values():
            spine.set_edgecolor("white")
            
        cb2 = plt.colorbar(plot2)
        cb1 = plt.colorbar(plot1)
        
        # COLORBAR
        # set colorbar label plus label color for agents
        cb2.set_label('amount of agents', color="black")
        cb1.set_label('amount of food per field', color="black")
        # set colorbar tick color
        cb2.ax.yaxis.set_tick_params(color="black")
        cb1.ax.yaxis.set_tick_params(color="black")
        
        # set colorbar edgecolor 
        cb2.outline.set_edgecolor("white")
        cb1.outline.set_edgecolor("white")
        
        # set colorbar ticklabels
        plt.setp(plt.getp(cb2.ax.axes, 'yticklabels'), color="black")
        plt.setp(plt.getp(cb1.ax.axes, 'yticklabels'), color="black")

        
        plt.title("Distribution of food and agents in the world",color = "black")
        plt.show()
        
        #showing food array to check visualization (optional)
        #print(self.board.food)
        #showing world array to check visualization (optional)
        #print(self.board.world)
        
        #showing number of angents still living
        print(f"number of agents: {len(self.board.agents_list)}")
        
        #checking if there is food left in the world
        #if not agents will probably die in a couple of rounds
        if self.board.food.any() >=1 :
            print('still some food left')
        else:
            print("no food left")            
    
            
# Counter einfügen wie oft sich ein Agents fortgepflanzt hat 
# Stammesangehörigkeit ausbessern: Aktuell Tupel für Stamm des Kindes

start = time.time()

if __name__ == "__main__":
    game = Game()
    game.run()

end = time.time()

timee = end-start
print(timee)
