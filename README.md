<img width="500" height = "300" alt="genetic_alg" <img alt="genetic_alg" src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/eb9d936e-5e26-4106-a8c3-dcde95f36305">

#  User & Developer Documentation for the Project „Genetic Algorithms Simulation based on the NumPy-Arrays“. 

**Assignment Description:**
https://moodle.hs-duesseldorf.de/pluginfile.php/461132/mod_resource/content/0/Projektauftrag_Genetic_algorithm.pdf


![GitHub repo size](https://img.shields.io/github/repo-size/SophZoe/Genetic_Algorithm) ![GitHub License](https://img.shields.io/github/license/SophZoe/Genetic_Algorithm) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/SophZoe/Genetic_Algorithm/main.yml) ![Python Version](https://img.shields.io/badge/python-3.11%20and%20below-blue)

                                
## System Requirements

- Python 3.3 and below
- NumPy Module
- Matplotlib Library (for plotting the rounds)
- Numba Library (optional for performance optimization)

## Installation

Make sure that Python and the required libraries are installed on your system. You can install them using the pip:
pip install random
pip install numpy
pip install matplotlib
pip install numba

To work with this repository follow these steps: 

1. **Clone the repository**

```bash
git clone https://github.com/SophZoe/Genetic_Algorithm
```
. 2. **Navigate to the Project directory on your Terminal or CMD**

```bash
cd /Genetic_Algorithm/MAINCODE
```
. 3. **Run Locally**

Open the main.py in any IDE of your choice.

## Game Concept
This simulation game reproduces the behavior of agents (living beings) in a virtual world. Each agent has energy, genetic inheritance features, can move, consumes food, which increases their energy score, and reproduce. The world is organized as a two-dimensional field (default 100x100) on which food is randomly placed. The simulation runs through several rounds (up to 100) in which agents act until they either die or the maximum number of rounds is reached. Reproduction works as follows:
firstly the  energy costs will be accounted, secondly the success rate based on strain affiliation is to be added, and the transfer (inheritance) of genetic traits from parents to offspring takes place, resulting in a diverse and dynamic population of agents over time.

**Starting the simulation**
To start the simulation, the Python code must be executed. The code automatically initializes a game instance and runs the simulation with the preset parameters.

**End of the simulation**
At the end of the simulation, the execution time is displayed in seconds. If saving is activated, the agent data is saved in a CSV file in the "results" folder. The file contains information on each agent, including strain affiliation, condition, visibility, reproduction counter, consumption counter, position and lifespan.

## Global variables and Settings
The simulation uses a set of constants to define the behavior and environment of the agents:

ENERGYCOSTS_MOVEMENT: the energy cost of moving an agent.
ENERGYCOSTS_REPRODUCTION: The energy costs for reproduction.
START_ENERGY: The starting energy of an agent.
WIDTH, HEIGHT: The dimensions of the board.
NUMBER_AGENTS: The initial number of agents.
ROUNDS: The number of simulation rounds.
ENERGY_FOOD: The amount of energy provided by the food consumed.
FOOD_PERCENTAGE_BEGINNING: Percentage of randomly placed food at the beginning of the simulation. 
ADDITIONAL_FOOD_PERCENTAGE: The amount of additional food (in percentage) that is added in each new round.
SICKNESS_DURATION = ROUNDS: Sets the length of the immobilisation of the agents after they have eaten the poisonous food.

## Types of food
There have been a dictionary with 7 types of food created. Those foods are differentiated according to the 3 parameters, which are:
- **"Energy"** : The energy score that every agent wins after consuming a specific food type. Attention: the energy is not credited to agents right after they reach the same board field where the food lies but only after the "consumption_time" has been calculated based on the "Metabolism" rate.
-  **"consumption time"** is calculated by dividing the food's base "consumption time" by the agent's "Metabolism" value and has been introdused to gather information to what extent biologically determined attributes can benefit or impair the agents chances of survival. 
- "disease_risk": first three food types are non-poisonous and thus have the "disease_risk" = 0. The food types from 5 to 7 have the increasing rate of poisoning effect that results in immobilising the agent for 1 round. 
  <img width="448" alt="food" src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/c867b1fe-2290-4d37-ac70-f21f5092c946">


## Genes that determines the agents behaviour
"Condition": Ranges from 1 to 3. Given the same energy level an agent with the "Condition" gene expressed wto the maximum of  3 points can move a further distance across the board than an agent with the "Condition" = 1 or 2. 
"Visibilityrange": Represents an agent's ability to detect other objects and food on the board. The higher the "Visibilityrange" gene expression, the futher one can see around his position on the board. 
"Tribe": This gene categorizes agents into 3 different groups called "Tribes". During the reproduction process, the compatibility of two agents for successful reproduction is influenced by whether they share the same "Tribe" gene value. This simulates a form of social behavior or mating preference, where agents are more inclined to reproduce with those from the same Tribe. When two agents attempt to reproduce, their "Tribe" genes are compared. If the agents belong to the same tribe, the likelihood of successful reproduction is 100% (success_rate = 1). If they belong to different tribes, the success rate drops significantly to 30% (success_rate = 0.3). This mechanism encourages genetic diversity within the population while still allowing for some level of inter-tribal reproduction. Upon successful reproduction, the offspring inherits the "Tribe" gene from one of its parents, chosen at random. 
"Resistance": Determines how susceptible to the poisonous food an agent is. The higher the score, the lower "sickness_risk" calculated for a specific agent. The agents with a dominant 
"Metabolism": Determines how fast one agent can digest the consumed food.

The initial distribution of genes (genedistribution method) links "Intelligence to "Aggression", such that if an agent is intelligent (self.genetic["Intelligent"] == True), it is not aggressive (self.genetic["Aggressive"] = False). This setup implies that intelligence in agents is associated with non-aggressive behavior, indicating a strategic approach to survival that avoids unnecessary risks.
"Intelligent": Makes agents be able to detect poisonous food  and thus avoid consuming it, as well as to avoid direct interaction with agents with the "Agressive" gene. 
"Aggressive": Aggressive agents might implicitly have an advantage at food sources due to their willingness to engage in conflicts. However their are not able to tell apart the food type with high "sickness_risk" from the food with "sickness_risk" = 0 and thus are more prone to get immobilized for a round after consuming the poisonous food. 
<img width="251" alt="genpool" src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/e2cc09b0-62c3-4e54-a7dc-0c00fd518dfa">

## Code Structure
The code consists of several classes that model the agents, the game board and the game itself. The most important classes are:
- **Agent**: Represents a single agent with the properties energy, genetic traits and position. Methods of this class allow the agent to move, consume food and reproduce.
- **Board**: Manages the game board, including the position of food and agents. It allows the addition of food and the removal of agents.
- **Game**: Coordinates the simulation process, including initializing the game board, adding agents and conducting rounds.

## Important methods of each class and their functions**

**- Agent**
The Agent class represents the living being in the ecosystem with the following properties and methods:

**- __init__():** Initializes a new agent with a unique number, starting energy, random position and empty genetic profile.
- **genedistribution():** Assigns genetic properties from the GENPOOL to the agent.
**- consuming_food():** This method is a simulation of how an agent consumes food and the consequences of that action, including the time it takes to consume the food, the energy gained, and the potential risk of disease that may come with the food. It also shows that the agent's genetic attributes play a significant role in these interactions, affecting both the efficiency of food consumption ("Metabolism") and the agent's susceptibility to disease ("Resistance").
**- move():** Moves the agent and consumes energy, updates the position of the agent and regulates the logic of the flight mode in the agents that stumble upon their agressive counterparts. 
**- search_food():** Searches for food near the agent. If food is within reach, the agent consumes it. Apart from that the search_food method includes logic where an agent checks for aggressive agents nearby before consuming food. If an aggressive agent is detected, a non-aggressive, intelligent agent may stop eating and move away to avoid conflict (self.move_away_from_aggressive(board, aggressive_agents_nearby)). This behavior suggests that intelligence equips agents with the foresight to avoid potentially dangerous situations, prioritizing safety.
**- check_for_aggressive_agents():** Activates the mechanism of detecting the aggressive agents by all the agents with (self.genetic["Aggressive"] = False).
**- move_away_from_aggressive():** Initiates the flight response where a non-aggressive agent, upon encountering aggressive agents, prioritizes its safety over continuing to consume food. By resetting the consumption_time to 0, the agent effectively stops eating and prepares to move away, with the flee_counter indicating how long this fleeing behavior will last.
**- reproduce():** Enables reproduction between two agents if they are on the same field and have enough energy.
**- genedistribution_throgh_heredity():** Determines the genetic traits of a newborn agent based on the parents' genes.

**- Board**
The board class manages the simulated world in which the agents live:

**- __init__():** Initializes the game board, a list for agents and a Zero-NumPy array for food distribution.
**- add_agent():** Adds a new agent to the world.
**- place_food():** Places food on the board based on a specified percentage of spaces
**- place_agents():** Places agents on the game board for the further visualization.
**- remove_agents():** Removes an agent from the game board.

**- Game**
The Game class controls the simulation process:
** - __init__():** Initializes the game on the game board and adds agents and food.
** - run():** Runs the specified number of simulation rounds in which agents move randomly. Coordinates reproduction and the search for food as well as placing additional food after every 10th round of the simulation.
** - save_data():** Saves the simulation data in a CSV file.

**- Visualization**
** - visualize_board():** Visualizes the world and the distribution of agents and food.
The method uses the Matplotlib library to visualize the state of a board in a simulation game, which consists of agents and food distributed on a grid (100x100). Defines a grid using NumPy's arange function. Includes the Agent counter display and checks if there is any food left on the board and how many agents are still living.

<img width="437" alt="Round 1 " src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/b7f4cf52-23f0-4009-8aad-7c1f6e202304">


## Customization and possible feature extension**
The structure of the code can be extended and changed dynamically. In particular, the initially defined constants can be adapted according to the conditions of a new world. Possible adaptations include
- Changing the energy costs for movement and reproduction,
- Agent behavior (possibly introducing agents that behave aggressively towards other agents,
- dynamics of the simulation (the game board could be scaled to speed up the execution time for the rounds),
- the introduction of new genetic traits,
- the adjustment of probabilities for diseases and the success rate for the reproduction, comparing the simulation dynamics if the random placement of food is replaced with the normal distribution of foof onevery board field. .

## Saving and analyzing the generated data
The option to save the simulation results in a CSV file enables the subsequent analysis and evaluation of the simulation runs in order to gain additional insights with regard to possible improvements/extensions of the simulation or to carry out data-related analyses.

<img width="795" alt="csv_results" src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/2f7e30c6-552a-433e-9c48-14bc286a4670">

## Tests and measures for the Continuous Integration of the code**
  
**General instructions for running the tests:**

Install pytest and make sure that all required libraries are installed.
Execute the tests with the pytest command in your terminal or integrated development environment (IDE).
Check the output for errors and make sure that all tests pass to ensure the integrity of the simulation code.
The tests are designed to cover the core functionality of the simulation code and ensure that the basic logic of agent movement, feeding, reproduction and inheritance works as intended. 

## Tests

**- test_add_agent**
Description: Checks whether an agent (living being) is initialized correctly with the intended start values.
Purpose: Ensures that the agents are created with the correct number, starting energy and a valid starting position within the game limits and that the propagation counter is set to 0.

**- test_genedistribution**
Description: Tests the gene distribution method of an agent.
Purpose: Confirms that the agent's genes are correctly assigned from the GENPOOL by checking that the keywords are present in the agent's genetics dictionary.

**- test_move**
Description: Checks the move method of an agent.
Purpose: Checks whether the agent moves (by changing position) or whether the agent's energy decreases after attempting to move if no movement occurs.

**- test_search_food**
Description: Tests whether an agent can successfully search for food on the board and increase its energy.
Purpose: Confirms that the search_food method increases the agent's energy if there is food at its position.

**- test_reproduction**
Description: Checks the reproduce method between two agents.
Purpose: Ensures that a new agent object is added to the agent list of the game board after the method is called and that the number of the new agent increases correctly.

**- test_gen_distribution_through_inheritance**
Description: Tests the inheritance of genes in the gene_distribution_through_inheritance method.
Purpose: Checks whether the genes of the offspring are correctly combined from the genes of the parents.

**- test_run**
Description: Tests the run method of the game.
Purpose: Validates that the game is executed without errors and runs through the simulation rounds.

**- test_save_data**
Description: Tests the save_data method of the game.
Purpose: Validates that the simulation results can be correctly written to a CSV file and that no errors occur.


## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for more details.

## Authors

- [@julietteyek] (https://github.com/julietteyek)
- [@Jxshyz] (https://github.com/Jxshyz)
- [@Markomrnkvc] (https://github.com/Markomrnkvc)
- [@SophZoe] (https://github.com/SophZoe)
- [@Salt-is-leaving] (https://github.com/Salt-is-leaving)
  




