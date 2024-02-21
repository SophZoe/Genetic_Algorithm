
#""" main.py but with world-comparison """
import random

import numpy as np
import csv
import matplotlib.pyplot as plt
import time
import random
from matplotlib.pyplot import imshow
from matplotlib import colormaps as cm
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import os

# Constants
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 10
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 10
ROUNDS = 10
FOOD_PERCENTAGE_BEGINNING = 0.1
ADDITIONAL_FOOD_PERCENTAGE = 0.1
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
        "Tribe": (1, 3), #what use? 
        "Resistance": (1, 3),
        "Metabolism": (1, 3),
        "Intelligent": [True, False],
        "Aggressive": [True, False]
    }
}

class Agent:
    """ 
     Class to represent an Agent in this simulated environment with various genetic traits and behaviours.
      
    Attributes
    ----------
    number : int
        unique identifier for agent
    \n
    energy : int
        current energy of agent
    \n
    genetic : dict
        genetic traits of agent
    \n
    position : touple
        current position of agent on board
    \n
    covered_distance : int
        distance covered by agent, starts at 0
    \n
    expelled : int
        number of times agent has been expelled, starts at 0
    \n
    flee_counter : int
        checks if agent is in flight mode, starts at 0
    \n
    consume_counter : int
        number of times agent has consumed food, starts at 0
    \n
    consumption_time : int
        time needed for agent to consume different food
    \n
    sick : bool
        initial health of agent, default set to false
    \n
    sickness_counter : int
        number of times agent has been sick, starts at 0
    \n
    sickness_duration : int
        duration of agents sickness
    \n
    previous_condition : int
        previous condition of agent, default set to none
    \n
    reproduction_counter : int
        number of times agent has reproduced with a partner, starts at 0
    \n
    parent_A : int
        unique identifier for agents parent A, default set to None
    \n
    parent_B : int
        unique identifier for agents parent B, default set to None

    Methods
    -------
    genedistribution():
        randomly sets the genedistribution of each agent based on predetermined genes
        in the global dictionary GENPOOL
    \n
    consuming_food(food_dict):
        adjusting health and status values of an agent based on food properties,
        which are predetermined through the food_dict and the agents unique genedistribution
    \n
    move(board):
        defines how the agent moves on the board considering the state it is in
        (linking the movement with it's energy, sickness and fleeing behaviour)
    \n
    search_food(board):
        finding food is defined through the agents gene 'visibility_range', if food is found it 
        will be consumed, considering the agents unique genedistributions and intelligence
        (disease risk) and the presence of aggressive agents
    \n
    check_for_aggressive_agents(board, x, y):
        ability of an agent to check for agressive agents within a specified search radius 
        from its given location; is called in the search_food method
    \n
    move_away_from_aggressive(board, aggressive_agents):
        agent will move away from aggressive agents, if any were found
        (if any were found with the check_for_aggressive_agents method), its food consumption
        is being interrupted
    \n
    reproduce(board, partner):
        agents that occupy the same position and have suficcient energy have a chance to reproduce,
        success is dependant on tribal affiliation, with a guarantee if they are frome the same 
        tribe. succesful reproduction results in a new agent inheriting genetic treits 
        from both parents (calling the genedistribution_thru_heredity method)
    \n
    genedistribution_thru_heredity(parent1, parent2):
        determines the genetic traits of an agent created through reproduction, combining traits
        from both parents, some selected at random (tribe, intelligence), others calculated
    """

    def __init__(self, number, sick=0):
        """
        Initializes all necessary attributes for the agent object
        
        Parameters
        ----------
        number : int
            unique identifier for agent
        sick : int
            initial health of agent, default set to 0

        Returns
        -------
        None
        """
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
        """
        randomly sets the genedistribution of each agent based on predetermined genes
        in the global dictionary GENPOOL

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
        """
        adjusting health and status values of an agent based on food properties, \n 
        which are predetermined through the food_dict and the agents unique genedistribution

        Parameters
        ----------
        food_dict : dict
            global dictionary with all food attributes listed
        
        Returns
        -------
        None
        """
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
        """
        defines how the agent moves on the board considering the state it is in

        Parameters
        ----------
        board : Any
            (right now board is not accessed in method)

        Returns
        -------
        Literal ["deceased"] if Agent died | None
        """
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
                    self.energy -= ENERGYCOSTS_MOVEMENT
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
        """
        finding food is defined through the agents gene 'visibility_range', if food is found it \n
        will be consumed, considering the agents unique genedistributions and intelligence \n
        (disease risk) and the presence of aggressive agents

        Parameters
        ----------
        board : Any

        Returns
        -------
        tuple [int, int] coordinates of the (consumed) food | None
        """
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
        """
        ability of an agent to check for agressive agents within a specified search radius \n
        any agent recognized as aggressive is appended to a list \n
        is called in the search_food method

        Parameters
        ----------
        board : Any
        x : int
        y : int

        Returns
        -------
        list() of aggressive agents

        """
        aggressive_agents = []
        search_radius = 2
        for agent in board.agents_list:
            if agent is not self and agent.genetic["Aggressive"]:
                distance = max(abs(agent.position[0] - x), abs(agent.position[1] - y))
                if distance <= search_radius:
                    aggressive_agents.append(agent)
        return aggressive_agents

    def move_away_from_aggressive(self, board, aggressive_agents):
        """
        agent will move away from aggressive agents, if any were found \n
        food consumption is stopped while the agent moves away

        Parameters
        ----------
        board : Any
        aggressive_agents : list

        Returns
        -------
        None
        """
        self.flee_counter = 5
        self.consumption_time = 0

    def reproduce(self, partner, board):
        """
        agents in the same position on the board have a chance to reproduce,\n 
        given certain circumstances (position, energy, tribe affiliation)\n
        every reproduction is tracked within the agent\n
        the child is added onto the board as an agent

        Parameters
        ----------
        board : Any
        partner : Any

        Returns
        -------
        None
        """
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
        """
        determines the genetic traits of an agent created through reproduction,\n
        combining traits from both parents, some selected at random (tribe, intelligence), others calculated

        Parameters
        ----------
        parent1 : Any
        parent2 : Any

        Returns
        -------
        None
        """
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
    """
    class to represent the board, on which the agents and food are placed/removed

    Attributes
    ----------
    width : int
        width of the board (cells along the x axis)
    \n
    height : int
        height of the board (cells along the y axis)
    \n    
    energy_costs_movement : int
        minimum amount of energy needed by the agent to move
    \n
    energy_costs_reproduction : int
        minimum amount of energy needed by the agent to reproduce
    \n
    start_energy : int
        initial amount of energy agent recieve when being created
    \n
    number_agents : int
        initial number of agents placed on board
    \n
    rounds : int
        how many rounds the simulation will run before ending
    \n
    food_percentage_beginning : float
        initial percentage of the board filled with food
    \n
    additional_food_percentage : float
        percentage of additional food being placed on the board each round
    \n
    sickness_duration : int
        number of rounds agent remains sick if inflicted with sickness
    
    Methods
    -------
    add_agent(agents_to_add):
        adds new agent(s) to an already existing list of agents
    \n
    place_agent():
        every agent in agent_list is placed on the board based on its position
    \n
    place_food(prozent):
        initially places random food randomly on the board and adds food each round\n
        according to additional_food_percentage
    \n
    remove_agent(agent):
        removes deceased agent from agents_list
    """

    def __init__(self, width=WIDTH, height=HEIGHT, energy_costs_movement=ENERGYCOSTS_MOVEMENT,
                 energy_costs_reproduction=ENERGYCOSTS_REPRODUCTION, start_energy=START_ENERGY,
                 number_agents=NUMBER_AGENTS, rounds=ROUNDS,
                 food_percentage_beginning=FOOD_PERCENTAGE_BEGINNING,
                 additional_food_percentage=ADDITIONAL_FOOD_PERCENTAGE,
                 sickness_duration=SICKNESS_DURATION, **kwargs):    # makes sure you can adjust individual parameters
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
        self.food_placement_counter = 0
        self.remove_agents_counter = 0

        self.agents_list = []
        self.food = np.zeros((width, height))
        self.world = np.zeros((width, height))

    def add_agent(self, agents_to_add):
        """
        adds new agent(s) to an already existing list of agents
        
        Parameters
        ----------
        agents_to_add : Any

        Returns
        -------
        None
        """
        self.agents_list.append(agents_to_add)

    def place_food(self, prozent):

        food_placed_this_round = 0

        """
        initially places random food randomly on the board and adds food each round\n
        according to additional_food_percentage

        Parameters
        ----------
        percent : float

        Returns
        -------
        None
        """

        amount_fields = int(self.width * self.height * prozent)
        for _ in range(amount_fields):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            food_key = random.choice(FOOD_KEYS)
            self.food[x][y] = food_key
            food_placed_this_round += 1

        print(f"Food placed this round: {food_placed_this_round}")
        self.food_placement_counter += 1

    def remove_agents(self, agent):
        """
        removes deceased agent from agents_list
        
        Parameters
        ----------
        agent : Any
        
        Returns
        -------
        None
        """
        self.agents_list.remove(agent)
        

    def place_agents(self):
        """
        every agent in agent_list is placed on the board based on its position\n
        clears the board every round and then re-places the updated agents\n
        using the agents in agents_list

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.world = np.zeros_like(self.world)

        for agent in self.agents_list:
            x, y = agent.position
            self.world[x][y] += 1

    def remove_agents(self, agent):
        self.agents_list.remove(agent)

class Game:
    """
    class to run the simulation allowing it to be modelled across multiple "worlds"\n
    visualizing the simulation and data collection for every round

    Attributes
    ----------
    saving : bool
        determines, if data for simulation is saved, default set to False
    \n
    worlds : int
        number of seperate simulated "worlds", default set to 1
    \n
    data_list : list
        list to store data for each simulated world
    \n
    board : Board
        instance of the Board class
    
    Parameters
    ----------
    **kwargs : dict
        unpack dict of keyword arguments passed to board
    
    Methods
    -------
    run():
        runs the simulation, iterating through number of worlds,\n
        each with a predefined number of rounds\n
        updates states of agents and food, optionally collects data for simulation\n
        ends simulation if no agents left or max number of rounds is reached
    \n
    collect_agent_data(board):
        collect and return data for each agent in agents_list
    \n
    save_data():
        saves collected data into seperate .csv files\n
        creates directory for collected data if none exists
    \n
    visualize_board():
        visualizes state of simulation for each round\n
        visualizes distribution of food and agents for each round
    """

    def __init__(self, saving=False, worlds=1, **kwargs):
        self.saving = saving
        self.worlds = worlds
        self.data_list = []
        self.board = Board(**kwargs)    # used "kwargs" to unpack the dict of keyword arguments and pass them to Board

    def run(self):
        """
        runs the simulation, iterating through number of worlds,\n
        each with a predefined number of rounds\n
        updates states of agents and food, optionally collects data for simulation\n
        ends simulation if no agents left or max number of rounds is reached

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for world in range(self.worlds):  # iterate over the specified number of worlds
            print(f"----------World {world + 1}------------")
            agents_counter = NUMBER_AGENTS  # separate counter for each world
            deceased_agents_counter = 0
            game_data = {'world': world + 1, 'agent_data': []}  # store data for each world

            # this now is configured for each world:
            # board = Board(WIDTH, HEIGHT)
            for i in range(1, NUMBER_AGENTS + 1):
                self.board.add_agent(Agent(i))

            self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
            self.board.place_agents()
            
            for round in range(ROUNDS):
                print(f"------------Round {round + 1}------------")
                round_deceased_agents = 0
                
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
                        self.remove_agents_counter += 1
                        round_deceased_agents += 1

                    else:
                        for partner in self.board.agents_list:
                            if agent != partner:
                                agent.reproduce(partner, self.board)
                deceased_agents_counter += round_deceased_agents
                print(f"Agents deceased this round: {round_deceased_agents}")
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                self.board.place_agents()
                self.visualize_board()
                """if round % 10 == 0:
                    self.visualize_board()"""

            self.board.place_agents()

            # If saving is on:
            # creates dict 'game_data' to store the data for the current game-world
            # then collects agent-data from the board and stores in 'game_data' under the key 'agent_data'
            if self.saving is True:
                pass
                game_data['agent_data'] = self.collect_agent_data(self.board)
                self.data_list.append(game_data)

        #PROBLEM---- this still necessary?
        if self.saving:
            pass
            #self.save_data()
        print(f"Food was placed {self.board.food_placement_counter} times during the simulation.")
        print(f"{self.board.remove_agents_counter} agents perished during the simulation.")
        print(f"Total deceased agents in world {world + 1}: {deceased_agents_counter}")


    def collect_agent_data(self, board):  # new method to collect agent-data
        """
        collect and return data for each agent in agents_list

        Parameters
        ----------
        board : Any

        Returns
        -------
        list() of agent_data
        """

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
                'parent_B': agent.parent_B,
                'genes': {
                    'Kondition': agent.genetic['Kondition'],
                    'Visibilityrange': agent.genetic['Visibilityrange'],
                    'Tribe': agent.genetic['Tribe'],
                    'Resistance': agent.genetic['Resistance'],
                    'Metabolism': agent.genetic['Metabolism'],
                    'Intelligent': agent.genetic['Intelligent'],
                    'Aggressive': agent.genetic['Aggressive']
                }
            })

        return agent_data



    def save_data(self):  # new: a separate CSV file is created for each world
        """
        saves collected data into seperate .csv files\n
        creates directory for collected data if none exists

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

    def save_data(self):
        csv_index = 0
        if not os.path.exists('results_worlds'):
            os.makedirs('results_worlds')

        for world_data in self.data_list:
            world_num = world_data['world']
            filename = f'results_worlds/world_{world_num}_data.csv'
            while os.path.exists(filename):
                csv_index += 1
                filename = os.path.join('results_worlds', f'{csv_index}_world_{world_num}_data.csv')

            with open(filename, 'w', newline='') as file:
                fieldnames = ['agent_number', 'reproduction_counter', 'consume_counter',
                               'sickness_counter', 'covered_distance', 'expelled', 'parent_A', 'parent_B']
                
                # add "fieldnames" for the Genes-dictionary keys
                fieldnames.extend(['Kondition', 'Visibilityrange', 'Tribe', 'Resistance', 'Metabolism', 'Intelligent', 'Aggressive'])

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for agent_data in world_data['agent_data']:
                    # flatten the 'genes' dictionary into separate columns
                    flat_agent_data = {**agent_data, **agent_data['genes']}

                    del flat_agent_data['genes']
                    writer.writerow(flat_agent_data)

            print(f"Data was saved: for world {world_num} in {filename}")

    def visualize_board(self):
        """
        visualizes state of simulation for each round\n
        visualizes distribution of food and agents for each round\n
        this is achieved by overlaying two heatmaps that visualize the density
        
        Parameters
        ----------
        food : Any
            not currently used in method
        
        Returns
        -------
        None
        """
        #5 seconds pause between each time visualizing 
        #time.sleep(2)
        
        plt.rcParams["figure.figsize"] = [7.50, 4.50]
        plt.rcParams["figure.autolayout"] = True
        
        dx, dy = 0.05, 0.05
        x = np.arange(-3.0, 3.0, dx)
        y = np.arange(-3.0, 3.0, dy)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)
        
        fig = plt.figure(frameon=False)
        
        
        
        #------changing colormaps so first value is lpotted white--------
        # Get the 'YlGn' colormap
        ylgn_cmap = cm.get_cmap('YlGn')
        
        # Get the colormap values
        ylgn_colors = ylgn_cmap(np.linspace(0, 1, 256))
        
        # Set the color at the beginning (where the value is 0) to white
        ylgn_colors[0] = [1, 1, 1, 1]  # [R, G, B, Alpha]
        
        # Create a new colormap with modified colors
        modified_YlGn = LinearSegmentedColormap.from_list('YlGn_modified', ylgn_colors)
        
        #get YlOrRd colormap
        YlOrRd_cmap= cm.get_cmap('YlOrRd')
        
        # Get the colormap values
        YlOrRd_colors = YlOrRd_cmap(np.linspace(0, 1, 256))
        
        # Set the color at the beginning (where the value is 0) to white
        YlOrRd_colors[0] = [1, 1, 1, 1]  # [R, G, B, Alpha]
        
        # Create a new colormap with modified colors
        modified_YlOrRd = LinearSegmentedColormap.from_list('YlOrRd_modified', YlOrRd_colors)
        
        
    
    
        data1 = self.board.food
        plot1 = imshow(data1, cmap= modified_YlGn, interpolation='nearest', extent=extent)
        
        data2 = self.board.world
        plot2 = imshow(data2, cmap= modified_YlOrRd, alpha = .7, interpolation='bilinear', extent=extent)
        
        
        # set imshow outline to white
        for spine in plot2.axes.spines.values():
            spine.set_edgecolor("white")
            
        cb2 = plt.colorbar(plot2)
        cb1 = plt.colorbar(plot1)
        
        # COLORBAR
        # set colorbar label plus label color for agents
        cb2.set_label('amount of agents', color="white")
        cb1.set_label('food ID', color="white")
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
        
        
        #showing number of angents still living
        print(f"number of agents: {len(self.board.agents_list)}")
        print(self.board.food)
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