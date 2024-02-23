"""
Genetic Algorithm - class_board.py

This module contains the board class, where all neccessary\n
attributes for the board are initialized and where agents&food\n
get placed or removed.

External Dependencies
---------------------
random
    random operations
numpy
    numerical operations
    data management

Authors
-------
    - [@julietteyek] (https://github.com/julietteyek)
    - [@Jxshyz] (https://github.com/Jxshyz)
    - [@Markomrnkvc] (https://github.com/Markomrnkvc)
    - [@SophZoe] (https://github.com/SophZoe)
    - [@Salt-is-leaving] (https://github.com/Salt-is-leaving)

"""
import random
import numpy as np
from src.main import *



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
    get_food_at_position(position):
        checks, if food is at position
    \n
    remove_agent(agent):
        removes deceased agent from agents_list
    """

    def __init__(self, width=WIDTH, height=HEIGHT,
                 energy_costs_movement=ENERGYCOSTS_MOVEMENT,
                 energy_costs_reproduction=ENERGYCOSTS_REPRODUCTION,
                 start_energy=START_ENERGY,
                 number_agents=NUMBER_AGENTS, rounds=ROUNDS,
                 food_percentage_beginning=FOOD_PERCENTAGE_BEGINNING,
                 additional_food_percentage=ADDITIONAL_FOOD_PERCENTAGE,
                 sickness_duration=SICKNESS_DURATION, **kwargs):
                # makes sure you can adjust individual parameters
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
        self.removed_agents_counter = 0

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

        food_placed_this_round = 0

        amount_fields = int(self.width * self.height * prozent)
        for _ in range(amount_fields):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            food_key = random.choice(FOOD_KEYS)
            if VISUALIZE_POISON == True:
                if FOOD[food_key]["disease_risk"] == 0:
                    self.food[x][y] = 1
                if FOOD[food_key]["disease_risk"] > 0:
                    self.food[x][y] = 2
            else:
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
        self.removed_agents_counter += 1
        
    def get_food_at_position(self, position):
        """
        checks, if food is at position
        
        Parameters
        ----------
        position : int
        
        Returns
        -------
        ndarray[Any, dtype] | None
        """
        x, y = position
        if self.food[x, y] != 0:  # Nimmt an, dass 0 bedeutet, dass kein Essen vorhanden ist
            food_key = self.food[x, y]
            return food_key  # Gibt den Schlüssel des Essens zurück
        return None  # Kein Essen an dieser Position

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
