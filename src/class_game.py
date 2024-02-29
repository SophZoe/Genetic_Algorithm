"""
Genetic_Algorithm - class_game.py

This module contains the game class, where all neccessary parameters\n
for the game are initialized which are needed to run the\n
simulation. The option to save and visualize the simulation\n
are also run from here.

External Dependencies
---------------------
os
    interaction with operating system
    file path management
csv
    writing .csv files
    allowing collected data export
numpy
    numerical operations
    data management
matplotlip
    plot and visualize gamestates in the simulation

Internal Dependencies
---------------------
class_board
    accesses class_board.py
class_agent
    accesses class_agent.py

Authors
-------
    - [@julietteyek] (https://github.com/julietteyek)
    - [@Jxshyz] (https://github.com/Jxshyz)
    - [@Markomrnkvc] (https://github.com/Markomrnkvc)
    - [@SophZoe] (https://github.com/SophZoe)
    - [@Salt-is-leaving] (https://github.com/Salt-is-leaving)
"""
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from class_board import Board
from class_agent import Agent
from main import *

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

    def __init__(self, VISUALIZE_POISON , saving=False, worlds=1, **kwargs):
        self.saving = saving
        self.worlds = worlds
        self.data_list = []
        self.VISUALIZE_POISON = VISUALIZE_POISON
        self.board = Board(**kwargs)
        self.removed_agents = 0
        #self.gui = GUI(board=self.board)

    # used "kwargs" to unpack the dict of keyword arguments and pass them to Board

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
        print(VISUALIZE_POISON)
        for world in range(self.worlds):  # iterate over the specified number of worlds
            print(f"\n\n----------World {world + 1}------------\n\n")
            AGENTS_COUNTER = NUMBER_AGENTS  # separate counter for each world
            deceased_agents_counter = 0
            game_data = {'world': world + 1, 'agent_data': []}  # store data for each world

            # this now is configured for each world:
            # board = Board(WIDTH, HEIGHT)
            for i in range(1, NUMBER_AGENTS + 1):
                self.board.add_agent(Agent(i, self.board))

            self.board.place_food(FOOD_PERCENTAGE_BEGINNING)
            self.board.place_agents()

            for round in range(ROUNDS):
                print(f"------------Round {round + 1}------------")
                self.visualize_board(VISUALIZE_POISON)
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

                        round_deceased_agents += 1


                    else:
                        for partner in self.board.agents_list:
                            if agent != partner:
                                agent.reproduce(partner, self.board)
                deceased_agents_counter += round_deceased_agents
                print(f"Agents deceased this round: {round_deceased_agents}")
                self.board.place_food(ADDITIONAL_FOOD_PERCENTAGE)
                self.board.place_agents()

                """if round % 10 == 0:
                    self.visualize_board()"""

            self.board.place_agents()

            # If saving is on:
            # creates dict 'game_data' to store the data for the current game-world
            # then collects agent-data from the board and stores in 'game_data'
            # under the key 'agent_data'
            if self.saving is True:
                game_data['agent_data'] = self.collect_agent_data(self.board)
                self.data_list.append(game_data)

            #resetting so the following worlds (if multiple in one simulation) start from scratch
            self.board.agents_list = []
            self.board.food = np.zeros_like(self.board.food)
            self.board.world = np.zeros_like(self.board.world)

        #PROBLEM---- this still necessary?
        if self.saving:
            self.save_data()
        print(f"Food was placed {self.board.food_placement_counter} times during the simulation.")
        #print(f"{self.removed_agents} agents perished during the simulation.")
        print(f"Total deceased agents in world {world+ 1}: {deceased_agents_counter}")


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
                'parent_A': agent.parent_a,
                'parent_B': agent.parent_b,
                'genes': {
                    'Condition': agent.genetic['Condition'],
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
        if not os.path.exists('Datascience/results_worlds'):
            os.makedirs('Datascience/results_worlds')

        for world_data in self.data_list:
            world_num = world_data['world']
            csv_index = 0
            filename = os.path.join('Datascience/results_worlds', f'{csv_index}___World({world_num}).csv')

            while os.path.exists(filename):
                csv_index += 1
                filename = os.path.join('Datascience/results_worlds/', f'{csv_index}___World({world_num}).csv')

            with open(filename, 'w', newline='', encoding="utf-8") as file:
                fieldnames = ['agent_number', 'reproduction_counter', 'consume_counter',
                               'sickness_counter', 'covered_distance', 'expelled',
                               'parent_A', 'parent_B']

                # add "fieldnames" for the Genes-dictionary keys
                fieldnames.extend(['Condition', 'Visibilityrange', 'Tribe', 'Resistance', 'Metabolism',
                                   'Intelligent', 'Aggressive'])

                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for agent_data in world_data['agent_data']:
                    # flatten the 'genes' dictionary into separate columns
                    flat_agent_data = {**agent_data, **agent_data['genes']}

                    del flat_agent_data['genes']
                    writer.writerow(flat_agent_data)

            #print(f"Data was saved: for world {world_num} in {filename}")
        return world_data


    def visualize_board(self, VISUALIZE_POISON):
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
        time.sleep(1)

        plt.rcParams["figure.figsize"] = [7.50, 4.50]
        plt.rcParams["figure.autolayout"] = True

        dx, dy = 0.05, 0.05
        x = np.arange(-3.0, 3.0, dx)
        y = np.arange(-3.0, 3.0, dy)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)

        fig = plt.figure(frameon=False)



        #------changing colormaps so first value is plotted white--------
        # Get the 'YlGn' colormap
        ylgn_cmap = cm.get_cmap('YlGn')

        # Get the colormap values3
        ylgn_colors = ylgn_cmap(np.linspace(0, 1, 256))

        # Set the color at the beginning (where the value is 0) to white
        ylgn_colors[0] = [1, 1, 1, 1]  # [R, G, B, Alpha]

        # Create a new colormap with modified colors
        modified_ylgn = LinearSegmentedColormap.from_list('YlGn_modified', ylgn_colors)

        #get YlOrRd colormap
        ylorrd_cmap= cm.get_cmap('YlOrRd')

        # Get the colormap values
        ylorrd_colors = ylorrd_cmap(np.linspace(0, 1, 256))

        # Set the color at the beginning (where the value is 0) to white
        ylorrd_colors[0] = [1, 1, 1, 1]  # [R, G, B, Alpha]

        # Create a new colormap with modified colors
        modified_ylorrd = LinearSegmentedColormap.from_list('YlOrRd_modified', ylorrd_colors)


        #color for visualization mode- intelligence
        colors_poison = ['white', 'green', 'purple']
        
        # Colormap for visualizing poisoned food
        cmap_poison = ListedColormap(colors_poison)
        
        #color for visualizing intelligent and aggresiv agents
        colors_intelligence = ['white', 'aqua', 'red']
        
        #colormap for visualizing intelligent and aggresiv agents
        cmap_intelligence = ListedColormap(colors_intelligence)

        data1 = self.board.food
        
        #setting bounds for norming values if needed
        bounds = [0, 0.5, 1.5,2]
        
        if VISUALIZE_POISON == True:
            # Erstellen einer Normalisierung, um Werte auf die Grenzen der Colormap abzubilden
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap_poison.N)
            #cb1.set_ticks([0, 1, 2])
            plot1 = imshow(data1, cmap= cmap_poison, interpolation='nearest', extent=extent, norm = norm)
        else:
            plot1 = imshow(data1, cmap= modified_ylgn, interpolation='nearest', extent=extent)

        data2 = self.board.world
        if VISUALIZING_INTELLIGENCE == True:
            # Erstellen einer Normalisierung, um Werte auf die Grenzen der Colormap abzubilden
            norm_intel = matplotlib.colors.BoundaryNorm(bounds, cmap_intelligence.N)
            plot2 = imshow(data2, cmap_intelligence,alpha = .7, interpolation='nearest', extent=extent, norm = norm_intel)
        else:
            plot2 = imshow(data2, cmap="YlOrRd",alpha = .7, interpolation='bilinear', extent=extent)
        
        """plot2 = imshow(data2, cmap= modified_ylorrd, alpha = .65,
                       interpolation='hanning', extent=extent)
        """
        
        # set imshow outline to white
        for spine in plot2.axes.spines.values():
            spine.set_edgecolor("white")

        

        # COLORBAR
        cb2 = plt.colorbar(plot2)
        cb1 = plt.colorbar(plot1)
        
        if VISUALIZING_INTELLIGENCE == True:
            cb2.set_label('    no agents    intelligent agents  agressiv agents', color="white")
            cb2.set_ticks([])
        else:
            cb2.set_label('amount of agents', color="white")
        
        # set colorbar label plus label color for agents
        if VISUALIZE_POISON == True:
            cb1.set_label('no food          non-poisonous          poisonous', color="white")
            
        else:
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
        #print(self.board.food)
        #checking if there is food left in the world
        #if not agents will probably die in a couple of rounds
        if self.board.food.any() >=1 :
            print('still some food left')
        else:
            print("no food left")
        
