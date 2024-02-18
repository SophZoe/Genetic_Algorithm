""" main.py but with world-comparison """
import random
import numpy as np
import csv
import matplotlib.pyplot as plt
import time
import os


# Constants
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 10
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 10
ROUNDS = 20
FOOD_PERCENTAGE_BEGINNING = 0.1
ADDITIONAL_FOOD_PERCENTAGE = 0
SICKNESS_DURATION = ROUNDS // 10


# Global counter for the numbering of living beings
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

GENPOOL = {
    "Genes": {
        "Kondition": (1, 3),
        "Visibilityrange": (1, 3),
        "Tribe": (1, 3),
        "Resistance": (1, 3),
        "Metabolism": (1, 3),
        "Intelligent": [True, False],
        "Aggressive": [True, False]
    }
}

class Agent:
    def __init__(self, number, sick=0):
        global agents_counter
        self.sickness_counter = 0
        self.number = number
        self.energy = START_ENERGY
        self.genetic = {}
        self.genedistribution()
        self.position = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        self.reproduction_counter = 0
        self.consume_counter = 0
        self.sick = False
        self.sickness_duration = 0
        self.flee_counter = 0
        self.previous_kondition = None
        self.parent_A = None
        self.parent_B = None
        self.consumption_time = 0
        self.covered_distance = 0
        self.expelled = 0

    def genedistribution(self):
        for gen, bereich in GENPOOL["Genes"].items():
            if isinstance(bereich[0], bool):
                self.genetic[gen] = random.choice(bereich)
                if self.genetic["Intelligent"] == True:
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True
            else:
                self.genetic[gen] = random.randint(*bereich)

    def consuming_food(self, food_dict):
        food = food_dict
        self.consumption_time = food_dict["consumption_time"] // max(1, self.genetic['Metabolism'])
        self.last_consumed_food_energy = food_dict["Energy"]
        risk = food["disease_risk"]
        if self.genetic["Intelligent"] is False:
            if random.random() < risk * (1 - self.genetic["Resistance"] / 3):
                self.sick = True
                self.sickness_duration = SICKNESS_DURATION
                self.sickness_counter += 1
                self.previous_kondition = self.genetic['Kondition']
                self.genetic["Kondition"] = 0

    def move(self, board):
        if self.consumption_time > 0:
            self.consumption_time -= 1  # Decrement the consumption timer
            # If consumption has just finished, add the energy from the last consumed food
            if self.consumption_time == 0:
                self.energy += self.last_consumed_food_energy   # Add the stored energy
                self.consume_counter += 1   # Increment the consume counter
                self.last_consumed_food_energy = 0  # Reset the stored energy to 0 for the next consumption
        else:
            if self.energy > ENERGYCOSTS_MOVEMENT:
                if self.sick is True:
                    self.check_for_sickness()

                    if self.flee_counter > 0:   # flight-mode
                        self.flee_counter -= 1

                        # random move: -1 or 1, multiplied with condition
                        dx = random.choice([-1, 1]) * self.genetic['Kondition']
                        dy = random.choice([-1, 1]) * self.genetic['Kondition']
                        new_x = max(0, min(WIDTH - 1, self.position[0] + dx))
                        new_y = max(0, min(HEIGHT - 1, self.position[1] + dy))
                        self.position = (new_x, new_y)
                else:
                    # random move: -1 or 1, multiplied with condition
                    dx = random.choice([-1, 1]) * self.genetic['Kondition']
                    dy = random.choice([-1, 1]) * self.genetic['Kondition']

                    new_x = max(0, min(WIDTH - 1, self.position[0] + dx))
                    new_y = max(0, min(HEIGHT - 1, self.position[1] + dy))
                    self.position = (new_x, new_y)
                    self.covered_distance += 1
            else:
                return "deceased"

    def search_food(self, board):
        visibilityrange = self.genetic["Visibilityrange"]
        for dx in range(-visibilityrange, visibilityrange + 1):
            for dy in range(-visibilityrange, visibilityrange + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                
                
                if 0 <= x < WIDTH and 0 <= y < HEIGHT and board.food[x][y] is not None:
                    food_dict = board.food[x][y]
                    # check if aggressive agents are nearby
                    aggressive_agents_nearby = self.check_for_aggressive_agents(board, x, y)

                    if aggressive_agents_nearby:
                        if not self.genetic["Aggressive"]:
                            # not-aggressive agent stops eating and moves away
                            self.consumption_time = 0   # stops the eating
                            self.move_away_from_aggressive(board, aggressive_agents_nearby)
                            self.expelled += 1
                            return None # go to next available food source

                    if self.genetic["Intelligent"] is True and food_dict["disease_risk"] == 0:
                        self.consuming_food(food_dict)
                        board.food[x][y] = None
                        return (x, y)
                    else:
                        self.consuming_food(food_dict)
                        board.food[x][y] = None
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
        self.flee_counter = 5
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
                if self.genetic["Intelligent"] == True:
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True


class Board:
    def __init__(self, width=WIDTH, height=HEIGHT, energy_costs_movement=ENERGYCOSTS_MOVEMENT,
                 energy_costs_reproduction=ENERGYCOSTS_REPRODUCTION, start_energy=START_ENERGY,
                 number_agents=NUMBER_AGENTS, rounds=ROUNDS,
                 food_percentage_beginning=FOOD_PERCENTAGE_BEGINNING,
                 additional_food_percentage=ADDITIONAL_FOOD_PERCENTAGE,
                 sickness_duration=SICKNESS_DURATION, **kwargs):
        self.width = width
        self.height = height
        self.energy_costs_movement = energy_costs_movement
        self.energy_costs_reproduction = energy_costs_reproduction
        self.start_energy = start_energy
        self.number_agents = number_agents
        self.rounds = rounds
        self.food_percentage_beginning = food_percentage_beginning
        self.additional_food_percentage = additional_food_percentage
        self.sickness_duration = sickness_duration

        self.agents_list = []
        self.food = np.zeros((width, height))
        self.world = np.zeros((width, height))

    def add_agent(self, agents_to_add):
        self.agents_list.append(agents_to_add)

    def place_food(self, prozent):
        amount_fields = int(self.width * self.height * prozent)
        for _ in range(amount_fields):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            food_key = random.choice(FOOD_KEYS)
            self.food[x][y] = food_key

    def remove_agents(self, agent):
        self.agents_list.remove(agent)

    def place_agents(self):
        self.world = np.zeros_like(self.world)

        for agent in self.agents_list:
            x, y = agent.position
            self.world[x][y] += 1

    def remove_agents(self, agent):
        self.agents_list.remove(agent)

class Game:
    def __init__(self, saving=False, worlds=1, **kwargs):
        self.saving = saving
        self.worlds = worlds
        self.data_list = []
        # used "kwargs" to unpack the dict of keyword arguments and pass them to Board
        # is useful when we want to use constants but also want to adjust them when calling the method
        self.board = Board(**kwargs)

    def run(self):
        for world in range(self.worlds):  # iterate over the specified number of worlds
            print(f"----------World {world + 1}------------")
            agents_counter = NUMBER_AGENTS  # separate counter for each world
            game_data = {'world': world + 1, 'agent_data': []}  # store data for each world

            # now this is configured for each world:
            #board = Board(WIDTH, HEIGHT)
            for i in range(1, NUMBER_AGENTS + 1):
                self.board.add_agent(Agent(i))

            self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
            self.board.place_agents()

            for round in range(ROUNDS):
                print(f"------------Round {round + 1}------------")
                
                # ending the simulation in case there are no agents left
                if len(self.board.agents_list) == 0:
                    print("--------------------------")
                    print("\nall agents deceased\n")
                    print("--------------------------")
                    break

                for agent in self.board.agents_list[:]:
                    # moves the agents
                    result = agent.move(self.board)

                    if result == "deceased":
                        self.board.remove_agents(agent)

                    else:
                        for partner in self.board.agents_list:
                            if agent != partner:
                                agent.reproduce(partner, self.board)

                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                self.board.place_agents()

                if round % 10 == 0:
                    self.visualize_board(FOOD)

            self.board.place_agents()

            # If saving is on:
            # creates dict 'game_data' to store the data for the current game-world
            # then collects agent-data from the board and stores in 'game_data' under the key 'agent_data'
            if self.saving is True:
                game_data['agent_data'] = self.collect_agent_data(self.board)
                self.data_list.append(game_data)

        #PROBLEM---- this still necessary?
        if self.saving:
            self.save_data()

    def collect_agent_data(self, board):  # new method to collect agent-data
        agent_data = []
        for agent in board.agents_list:
            agent_data.append({
                'agent_number': agent.number,
                'reproduction_counter': agent.reproduction_counter,
                'consume_counter': agent.consume_counter,
                'sickness_counter': agent.sickness_counter,
                'covered_distance': agent.covered_distance,
                'expelled': agent.expelled,
                'parent_A': agent.parent_A,
                'parent_B': agent.parent_B
            })
        return agent_data


    def save_data(self):  # new: a separate CSV file is created for each world
        if not os.path.exists('results_worlds'):
            os.makedirs('results_worlds')

        for world_data in self.data_list:
            world_num = world_data['world']
            filename = f'results_worlds/world_{world_num}_data.csv'

            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['agent_number', 'reproduction_counter', 'consume_counter',
                                 'sickness_counter', 'covered_distance', 'expelled', 'parent_A', 'parent_B'])

                for agent_data in world_data['agent_data']:
                    writer.writerow([agent_data['agent_number'], agent_data['reproduction_counter'],
                                     agent_data['consume_counter'], agent_data['sickness_counter'],
                                     agent_data['covered_distance'], agent_data['expelled'],
                                     agent_data['parent_A'], agent_data['parent_B']])

            print(f"Data was saved: for world {world_num} in {filename}")

    def visualize_board(self, food):
        #5 seconds pause between each time visualizing 
        #time.sleep(2)
        
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        
        dx, dy = 0.05, 0.05
        x = np.arange(-3.0, 3.0, dx)
        y = np.arange(-3.0, 3.0, dy)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)
        
        fig = plt.figure(frameon=False)



        data1 = self.board.food
        plot1 = plt.imshow(data1, cmap="YlGn", interpolation='nearest', extent=extent)
        
        data2 = self.board.world
        plot2 = plt.imshow(data2, cmap="YlOrRd",alpha = .7, interpolation='bilinear', extent=extent)
        
        
        # set imshow outline to white
        for spine in plot2.axes.spines.values():
            spine.set_edgecolor("white")
            
        cb2 = plt.colorbar(plot2)
        cb1 = plt.colorbar(plot1)
        
        # COLORBAR
        # set colorbar label plus label color for agents
        cb2.set_label('amount of agents', color="white")
        cb1.set_label('amount of food per field', color="white")
        # set colorbar tick color
        cb2.ax.yaxis.set_tick_params(color="white")
        cb1.ax.yaxis.set_tick_params(color="white")
        
        # set colorbar edgecolor 
        cb2.outline.set_edgecolor("white")
        cb1.outline.set_edgecolor("white")
        
        # set colorbar ticklabels
        plt.setp(plt.getp(cb2.ax.axes, 'yticklabels'), color="white")
        plt.setp(plt.getp(cb1.ax.axes, 'yticklabels'), color="white")

        
        plt.title("Distribution of food and agents in the world",color = "white")
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
            

if __name__ == "__main__":
    start = time.time()
    game = Game(saving=True, worlds=2, ROUNDS=10)
    #game = Game()
    game.run()
    script_time = np.round(time.time() - start, 2)
    print(script_time)
