"""CLASS Agent"""
import random
import main
import numpy as np

#from CLASS_Board import Board
#from CLASS_Game import Game

# Global counter for the numbering of living beings
agents_counter = main.NUMBER_AGENTS

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

    def __init__(self, number, board):
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
        for gen, bereich in main.GENPOOL["Genes"].items():
            if isinstance(bereich[0], bool):
                self.genetic[gen] = random.choice(bereich)
                if self.genetic["Intelligent"] == True:
                    self.genetic["Aggressive"] = False
                else:
                    self.genetic["Aggressive"] = True
            else:
                self.genetic[gen] = random.randint(*bereich)

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
        if self.consumption_time > 0:
            self.consumption_time -= 1  # Decrement the consumption timer
            # If consumption has just finished, add the energy from the last consumed food
            if self.consumption_time == 0:
                self.energy += self.last_consumed_food_energy   # Add the stored energy
                self.consume_counter += 1   # Increment the consume counter
                self.last_consumed_food_energy = 0  # Reset the stored energy to 0 for the next consumption
        else:
            if self.energy > main.ENERGYCOSTS_MOVEMENT:
                if self.sick is True:
                    self.check_for_sickness()

                    if self.flee_counter > 0:   # flight-mode
                        self.flee_counter -= 1

                        # random move: -1 or 1, multiplied with condition
                        dx = random.choice([-1, 1]) * self.genetic['Kondition']
                        dy = random.choice([-1, 1]) * self.genetic['Kondition']
                        new_x = max(0, min(main.WIDTH - 1, self.position[0] + dx))
                        new_y = max(0, min(main.HEIGHT - 1, self.position[1] + dy))
                        self.position = (new_x, new_y)
                        self.energy -= (main.ENERGYCOSTS_MOVEMENT*2)

                    else:
                        self.search_food(self.board)
                        self.energy -= (main.ENERGYCOSTS_MOVEMENT*2)
                else:
                    if self.flee_counter > 0:   # flight-mode
                        self.flee_counter -= 1

                        # random move: -1 or 1, multiplied with condition
                        dx = random.choice([-1, 1]) * self.genetic['Kondition']
                        dy = random.choice([-1, 1]) * self.genetic['Kondition']
                        new_x = max(0, min(main.WIDTH - 1, self.position[0] + dx))
                        new_y = max(0, min(main.HEIGHT - 1, self.position[1] + dy))
                        self.position = (new_x, new_y)
                        self.energy -= main.ENERGYCOSTS_MOVEMENT

                    else:
                        self.search_food(self.board)
                        self.energy -= main.ENERGYCOSTS_MOVEMENT
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
        if self.energy > main.ENERGYCOSTS_REPRODUCTION and self.position == partner.position:
            success_rate = 1 if self.genetic["Tribe"] == partner.genetic["Tribe"] else 0.3
            if random.random() < success_rate:
                agents_counter += 1
                kind = Agent(agents_counter, self.board)
                kind.genedistribution_thru_heredity(self, partner)
                self.energy -= main.ENERGYCOSTS_REPRODUCTION
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
        for gen in main.GENPOOL["Genes"]:
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