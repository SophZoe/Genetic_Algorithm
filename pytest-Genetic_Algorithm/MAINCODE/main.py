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
START_ENERGY = 10
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 10
ROUNDS = 50
ENERGY_FOOD = 5
FOOD_PERCENTAGE_BEGINNING = 0.1
ADDITIONAL_FOOD_PERCENTAGE = 0.1

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
            
            
    def place_agents(self):
        #deleting the array so deceased agents will not be shown
        self.world = np.zeros_like(self.world)
        
        #placing agents in array
        for agent in self.agents_list:
            x, y = agent.position
            self.world[x][y] += 1
        
    def remove_agents(self, agent):
        #removing the agents in the list 'lebewesen'
        self.agents_list.remove(agent)

class Game:
    def __init__(self):
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
            
            
            for agent in self.board.agents_list[:]:
                
                #bewegt die agents
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
                
                
            if round % 10 == 0:
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                self.board.place_agents()
                self.visualize_board()
                
                
               
            
        self.board.place_agents()  
        #visualisieren des boardes
        self.visualize_board()  
            ### Mögliches Laufzeitproblem: Doppelte For-Schleife sorgt für Quadratische Laufzeit O(n2)
            
        #saving data in csv
        #self.safe_data()

    def safe_data(self):
        with open('agents_daten.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Number', 'Tribe', 'Kondition', 'Visibilityrange', 'Fortpflanzungs-Counter', 'Position'])
            for agent in self.board.agents_list:
                writer.writerow([agent.number, agent.genetic['Tribe'], agent.genetic['Kondition'], agent.genetic['Visibilityrange'], agent.reproduction_counter, agent.position])
    def visualize_board(self):
        #5 seconds pause between each time visualizing 
        time.sleep(5)
        
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        
        dx, dy = 0.05, 0.05
        x = np.arange(-3.0, 3.0, dx)
        y = np.arange(-3.0, 3.0, dy)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)
        
        fig = plt.figure(frameon=False)
        
        data1 = self.board.food
        plt.imshow(data1, cmap="YlGn", interpolation='nearest', extent=extent)
        
        data2 = self.board.world
        plt.imshow(data2, cmap="YlOrRd",alpha = .7, interpolation='bilinear', extent=extent)
        
        plt.show()
        
        #imshow(self.board.food, cmap='YlGn', vmin = 0,alpha=.9, interpolation='bilinear', extent=extent)
        #plt.title('Food Distribution')
        #plt.show()
        
        #imshow(self.board.world, cmap = 'YlOrRd', vmin = 0, interpolation='nearest', extent=extent)
        #plt.title('Agents per field')
        #plt.show()
        
        plt.show()
        
        #showing food array
        #print(self.board.food)
        #showing world array
        #print(self.board.world)
        #showing number of angents still living
        print(f"number of agents: {len(self.board.agents_list)}")
        food_count = 0
        if self.board.food.any() >=1 :
            print(f'still some food left')
        else:
            print("no food left")            
    """def visualize_board(self):
        time.sleep(5)
        imshow(self.board.food, cmap='YlGn', vmin = 0)
        plt.title('Food Distribution')
        plt.show()
        
        imshow(self.board.world, cmap = 'YlOrRd', vmin = 0)
        plt.title('Agents per field')
        plt.show()
        
        #showing food array
        #print(self.board.food)
        #showing world array
        #print(self.board.world)
        
        #showing number of angents still living
        print(f"number of agents: {len(self.board.agents_list)}")
        
        #checking amount of food to see if there is some left in the world
        food_count = 0
        if self.board.food.any() >=1 :
            print(f'still some food left')
        else:
            print("no food left")"""
            
# Counter einfügen wie oft sich ein Agents fortgepflanzt hat 
# Stammesangehörigkeit ausbessern: Aktuell Tupel für Stamm des Kindes

start = time.time()

if __name__ == "__main__":
    game = Game()
    game.run()

end = time.time()

timee = end-start
print(timee)