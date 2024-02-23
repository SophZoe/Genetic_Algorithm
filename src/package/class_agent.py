"""
Genetic Algorithm - agent.py

This module contains the agent class, where all necessary\n
attributes for the agent object are initialized.


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
import main


#from CLASS_Board import Board
#from CLASS_Game import Game

# Global counter for the numbering of living beings
AGENTS_COUNTER = main.NUMBER_AGENTS

class Agent:
    """
     Class to represent an Agent in this simulated environment\n
     with various genetic traits and behaviours.

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
    parent_a : int
        unique identifier for agents parent A, default set to None
    \n
    parent_b : int
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
    check_for_sickness():
        checks if and how long the agent is sick, if False agents go back to previous condition
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
        from both parents (calling the genedistribution_through_heredity method)
    \n
    genedistribution_through_heredity(parent1, parent2):
        determines the genetic traits of an agent created through reproduction, combining traits
        from both parents, some selected at random (tribe, intelligence), others calculated
    """

    def __init__(self, number, board):
        """
        Initializes all necessary attributes for the agent object

        Parameters
        ----------
        number : int
            unique identifier for agent

        Returns
        -------
        None
        """
        global AGENTS_COUNTER
        self.board = board
        self.sickness_counter = 0
        self.number = number
        self.energy = main.START_ENERGY
        self.genetic = {}
        self.genedistribution()
        self.position = (random.randint(0, main.WIDTH - 1), random.randint(0, main.HEIGHT - 1))
        self.reproduction_counter = 0
        self.consume_counter = 0
        self.sick = False
        self.sickness_duration = 0
        self.flee_counter = 0
        self.previous_kondition = None
        self.parent_a = None
        self.parent_b = None
        self.consumption_time = 0
        self.covered_distance = 0
        self.expelled = 0
        self.last_consumed_food_energy = 0

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
        for gen, area in main.GENPOOL["Genes"].items():
            if isinstance(area[0], bool):
                self.genetic[gen] = random.choice(area)
                if self.genetic["Intelligent"] == True:
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True
            else:
                self.genetic[gen] = random.randint(*area)

    def consuming_food(self, food_key):
        """
        adjusting health and status values of an agent based on food properties, \n
        which are predetermined through the food_dict and the agents unique genedistribution

        Parameters
        ----------
        food_key : key
            a key used as reference for food

        Returns
        -------
        None
        """
        self.consumption_time = main.FOOD[food_key]["consumption_time"] // max(1, self.genetic['Metabolism'])
        self.last_consumed_food_energy = main.FOOD[food_key]["Energy"]
        risk = main.FOOD[food_key]["disease_risk"]
        if self.genetic["Intelligent"] is False:
            if random.random() < risk * (1 - self.genetic["Resistance"] / 3):
                self.sick = True
                self.sickness_duration = main.SICKNESS_DURATION
                self.sickness_counter += 1
                self.previous_kondition = self.genetic['Kondition']
                self.genetic["Kondition"] = 0

    def check_for_sickness(self):
        """
        checks if and how long the agent is sick, if False agents go back to previous condition

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.sick:
            self.sickness_duration -= 1
            if self.sickness_duration <= 0:
                self.sick = False
                self.genetic["Kondition"] = self.previous_kondition

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
        aggressive_agents_nearby = self.check_for_aggressive_agents(board)

        if aggressive_agents_nearby:
            self.consumption_time = 0
            #print("Agent moved away from aggressive")
            self.move_away_from_aggressive()
            self.expelled += 1
        elif self.consumption_time > 0:
            # Der Agent konsumiert gerade Nahrung
            self.consumption_time -= 1
            print("Agent konsumierte")
            if self.consumption_time == 0:
                print("Agent konsumierte 2.schleife")
                self.energy += self.last_consumed_food_energy
                self.consume_counter += 1
                self.last_consumed_food_energy = 0
        elif self.sick is True:
            #print("Agent checkt sickness:")
            self.check_for_sickness()  
        else:
            # Der Agent sucht nach Essen, wenn er nicht flieht oder Nahrung konsumiert
            #print("Agent searche jetzt food:")
            closest_food = self.search_food(board)
            if closest_food is not None:
                # Bewege den Agenten in Richtung des nächsten Essens
                #print("Agent bewegt sich richtung closest food")
                self.move_towards(closest_food)
            else:
                # Zufällige Bewegung, wenn kein Essen gefunden wird
                #print("Agent macht random move")
                self.random_move()

            # Reduziert die Energie nach der Bewegung
            self.energy -= main.ENERGYCOSTS_MOVEMENT if not self.sick else main.ENERGYCOSTS_MOVEMENT * 2
            if self.energy <= 0:
                return "deceased"

    def move_towards(self, food_position):
        # Kondition des Agenten
        kondition = self.genetic['Kondition']

        # Zielposition des Essens
        food_x, food_y = food_position

        # Berechne den effektiven Bewegungsschritt unter Berücksichtigung der Kondition
        step_x = min(abs(food_x - self.position[0]), kondition) * (1 if food_x > self.position[0] else -1)
        step_y = min(abs(food_y - self.position[1]), kondition) * (1 if food_y > self.position[1] else -1)

        # Aktualisiere die Position des Agenten
        new_x = self.position[0] + step_x
        new_y = self.position[1] + step_y

        # Stelle sicher, dass die neue Position innerhalb der Grenzen liegt
        new_x = max(0, min(main.WIDTH - 1, new_x))
        new_y = max(0, min(main.HEIGHT - 1, new_y))

        # Prüfe, ob auf der neuen Position Essen vorhanden ist
        food_key = self.board.get_food_at_position((new_x, new_y))
        if food_key:
            # Konsumiere das Essen und aktualisiere die Energie des Agenten
            self.consuming_food(food_key)
            # Entferne das Essen vom Board
            self.board.food[new_x, new_y] = 0

        # Aktualisiere die Position des Agenten
        self.position = (new_x, new_y)

    def random_move(self):
        # Führt eine zufällige Bewegung durch
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        new_x = max(0, min(main.WIDTH - 1, self.position[0] + dx))
        new_y = max(0, min(main.HEIGHT - 1, self.position[1] + dy))
        self.position = (new_x, new_y)

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

        # create a grid over the fields in the visibility range
        y_range, x_range = np.ogrid[-visibilityrange:visibilityrange+1, -visibilityrange:visibilityrange+1]

        # calculate the distance from each point in the grid to the current position of the agent
        distances = np.sqrt(x_range**2 + y_range**2)

        # create a boolean grid that is True where food is present
        food_mask = np.zeros_like(distances, dtype=bool)

        # check which points are within bounds and where there is food
        for dy in range(-visibilityrange, visibilityrange + 1):
            for dx in range(-visibilityrange, visibilityrange + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < main.WIDTH and 0 <= y < main.HEIGHT and board.food[x][y] != 0:
                    food_mask[dy + visibilityrange, dx + visibilityrange] = True

        # apply the food mask to the distances, set all others to infinity
        distances = np.where(food_mask, distances, np.inf)

        # find the position of the minimum distance
        min_distance_idx = np.argmin(distances)
        if distances.flat[min_distance_idx] == np.inf:
            return None  # no food found

        # calculate the relative position of the nearest food source
        dy, dx = np.unravel_index(min_distance_idx, distances.shape)
        closest_food = (dx - visibilityrange, dy - visibilityrange)

        return closest_food

    def check_for_aggressive_agents(self, board):
        """
        ability of an agent to check for agressive agents within a specified search radius \n
        any agent recognized as aggressive is appended to a list \n
        is called in the search_food method

        Parameters
        ----------
        board : Any

        Returns
        -------
        list() of aggressive agents
        """
        aggressive_agents_nearby = []
        search_radius = 2  # Definiert den Suchradius

        # Durchläuft alle Agenten im Board, um aggressive Agenten zu finden
        for agent in self.board.agents_list:
            if agent is not self and agent.genetic["Aggressive"]:
                # Berechnet die Distanz zwischen dem aktuellen Agenten und anderen Agenten
                distance = max(abs(agent.position[0] - self.position[0]), abs(agent.position[1] - self.position[1]))
                if distance <= search_radius:
                    aggressive_agents_nearby.append(agent)

        return aggressive_agents_nearby

    def move_away_from_aggressive(self):
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
        global AGENTS_COUNTER
        if self.energy > main.ENERGYCOSTS_REPRODUCTION and self.position == partner.position:
            success_rate = 1 if self.genetic["Tribe"] == partner.genetic["Tribe"] else 0.3
            if random.random() < success_rate:
                AGENTS_COUNTER += 1
                child = Agent(AGENTS_COUNTER, self.board)
                child.genedistribution_through_heredity(self, partner)
                self.energy -= main.ENERGYCOSTS_REPRODUCTION
                self.reproduction_counter += 1
                partner.reproduction_counter += 1
                board.add_agent(child)

    def genedistribution_through_heredity(self, parent1, parent2):
        """
        determines the genetic traits of an agent created through reproduction,\n
        combining traits from both parents, some selected at random (tribe, intelligence),\n
        others calculated

        Parameters
        ----------
        parent1 : Any
        parent2 : Any

        Returns
        -------
        None
        """
        for gen in main.GENPOOL["Genes"]:
            if gen == "Tribe":
                self.genetic[gen] = random.choice([parent1.genetic[gen], parent2.genetic[gen]])
                self.parent_a = parent1.number
                self.parent_b = parent2.number
            elif gen == "Intelligent":
                self.genetic[gen] == random.choice([parent1.genetic[gen], parent2.genetic[gen]])
            else:
                weight = random.uniform(0, 1)
                gen_value = (weight * parent1.genetic[gen] + (1 - weight) * parent2.genetic[gen]) / 2
                self.genetic[gen] = int(round(gen_value, 3))
                if self.genetic["Intelligent"] == True:
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True
