import pytest
from src.class_agent import Agent
from src.class_game import Game
from src.class_board import Board
from src.main import GENPOOL, START_ENERGY, WIDTH, HEIGHT, ENERGYCOSTS_REPRODUCTION, ROUNDS, FOOD_PERCENTAGE_BEGINNING
import os
import numpy as np

# ----------------------   AGENT  ----------------------
def test_agent_initialization():
    board = Board(WIDTH, HEIGHT)
    food = np.zeros(WIDTH, HEIGHT)  #return Board() ?
    agent = Agent(1)
    assert agent.number == 1
    assert agent.energy == START_ENERGY
    assert agent.sick is False
    # More checks for more attributes

def test_agent_genedistribution():
    agent = Agent(1)
    agent.genedistribution()
    # Check if gene-values are within expected range:
    for gene, (min_value, max_value) in GENPOOL["Genes"].items():
        assert min_value <= agent.genetic[gene] <= max_value or isinstance(agent.genetic[gene], bool)

#Tests for the method def consuming_food()
def test_consuming_food_no_sickness(agent):
    food_key = 1.0  # Choosing a food item with 0 disease risk
    agent.consuming_food(food_key)
    assert agent.consumption_time == FOOD[food_key]['consumption_time'] // agent.genetic['Metabolism']
    assert agent.last_consumed_food_energy == FOOD[food_key]['Energy']
    assert not agent.sick  # Agent should not become sick given the 0 disease risk

def test_consuming_food_with_sickness(agent):
    # Directly manipulating the agent's resistance or condition to ensure sickness outcome
    agent.genetic['Resistance'] = 0  # Ensuring no resistance
    food_key = 7.0  # Choosing a food item with the highest disease risk
    agent.consuming_food(food_key)
    # Assuming the risk is high enough, the agent should become sick
    assert agent.sick  # Agent becomes sick due to high disease risk
    assert agent.sickness_duration == SICKNESS_DURATION
    assert agent.sickness_counter == 1
    assert agent.previous_condition == agent.genetic['Condition']
    assert agent.genetic["Condition"] == 0  # Condition drops to 0 due to sickness 
    
#Tests for the method def check_for_sickness()
def sick_agent():
    # Setup a sick agent for testing
    genetic = {'Metabolism': 2, 'Intelligent': False, 'Resistance': 1, 'Condition': 5}
    agent = Agent(genetic=genetic)
    agent.sick = True
    agent.sickness_duration = 1  # Setting sickness duration to 1 for testing recovery
    agent.previous_condition = 11  # Setting a previous condition to test recovery
    return agent

def healthy_agent():
    # Setup a healthy agent for testing
    genetic = {'Metabolism': 2, 'Intelligent': False, 'Resistance': 1, 'Condition': 5}
    agent = Agent(genetic=genetic)
    agent.sick = False
    return agent

def test_check_for_sickness_recovery(sick_agent):
    sick_agent.check_for_sickness()
    assert not sick_agent.sick, "Agent should recover from sickness"
    assert sick_agent.sickness_duration == 0, "Sickness duration should be 0 after recovery"
    assert sick_agent.genetic["Condition"] == sick_agent.previous_condition, "Agent should return to previous condition after recovery"

def test_check_for_sickness_no_change(healthy_agent):
    initial_condition = healthy_agent.genetic["Condition"]
    healthy_agent.check_for_sickness()
    assert not healthy_agent.sick, "Healthy agent should remain not sick"
    assert healthy_agent.genetic["Condition"] == initial_condition, "Condition should not change for healthy agent"

def test_sick_agent_stays_sick(sick_agent):
    # Adjusting the sickness duration to test decrement
    sick_agent.sickness_duration = 2
    sick_agent.check_for_sickness()
    assert sick_agent.sick, "Agent should still be sick"
    assert sick_agent.sickness_duration == 1, "Sickness duration should decrement by 1"

#Tests for the method def move()
def moving_agent():
    # Constanta for tests
    ENERGYCOSTS_MOVEMENT = 1  # Assuming an energy cost constant is defined somewhere

    # Setup a default agent for testing
    genetic = {'Intelligent': False, 'Metabolism': 1, 'Resistance': 1, 'Condition': 1}
    agent = Agent(genetic=genetic)
    agent.energy = 10  # Setting default energy for movement tests
    agent.flight_mode = 0
    agent.consumption_time = 0
    agent.sick = False
    agent.expelled = 0
    agent.flight_mode = 0
    agent.last_consumed_food_energy = 0
    agent.consume_counter = 0
    return agent

def test_move_deceased_due_to_starvation(agent):
    agent.energy = 1  # Set energy to be depleted after one move
    status = agent.move(board) 
    assert status == "deceased", "Agent should be marked as deceased if energy depletes to 0"

def test_move_with_intelligent_agent_avoiding_aggression(agent, mocker):
    agent.genetic["Intelligent"] = True
    mocker.patch.object(agent, 'check_for_aggressive_agents', return_value=True)
    mocker.patch.object(agent, 'move_away_from_aggressive')
    mocker.patch.object(agent, 'random_move')
    agent.move(board)
    assert agent.expelled == 1, "Expelled counter should increment when avoiding aggression"
    assert agent.flight_mode == 0, "Flight mode should be unchanged if not initially set"

def test_move_in_flight_mode(agent, mocker):
    agent.flight_mode = 1
    mocker.patch.object(agent, 'random_move')
    agent.move(board)
    assert agent.flight_mode == 0, "Flight mode should decrement after moving"

def test_move_while_consuming_food(agent):
    agent.consumption_time = 2
    agent.last_consumed_food_energy = 5
    agent.move(board)
    assert agent.consumption_time == 1, "Consumption time should decrement after moving"
    if agent.consumption_time == 0:
        assert agent.energy == 15, "Agent energy should increase after consuming food"
        assert agent.consume_counter == 1, "Consume counter should increment after finishing food"

#Tests for the method def search_for_food()
def test_search_food_with_food_within_range(agent, board):
    
    # Setup a default agent for testing
    genetic = {'Visibilityrange': 2}  # Adjust visibility range as needed
    agent = Agent(genetic=genetic)
    agent.position = (50, 50)  # Setting default position for the agent
    return agent
    
    # Place food within the agent's visibility range
    board.food[51][52] = 1  # Adjust coordinates as needed within the agent's visibility range
    closest_food = agent.search_food(board)
    assert closest_food == (1, 2), "The method should return the relative position of the closest food"

def test_search_food_with_no_food_within_range(agent, board):
    # Ensure there's no food within the agent's visibility range
    closest_food = agent.search_food(board)
    assert closest_food is None, "The method should return None if no food is found within the visibility range"

def test_search_food_with_food_outside_range(agent, board):
    # Place food outside the agent's visibility range
    board.food[60][60] = 1  # Adjust coordinates to be outside the agent's visibility range
    
    closest_food = agent.search_food(board)
    assert closest_food is None, "The method should return None if food is outside the visibility range"
  
def test_agent_reproduce():
    agent1 = Agent(1, energy=ENERGYCOSTS_REPRODUCTION + 1, position=(0, 0), genetic={"Tribe": 1})
    agent2 = Agent(2, energy=ENERGYCOSTS_REPRODUCTION + 1, position=(0, 0), genetic={"Tribe": 1})

    # add agents to board
    board = Board()
    board.add_agent(agent1)
    board.add_agent(agent2)

    # test the success of reproduction
    agent1.reproduce(agent2, board)
    assert len(board.agents_list) == 3

    # check if energy of parents were reduced
    assert agent1.energy == 1  # ENERGYCOSTS_REPRODUCTION + 1 - ENERGYCOSTS_REPRODUCTION
    assert agent2.energy == 1  # ENERGYCOSTS_REPRODUCTION + 1 - ENERGYCOSTS_REPRODUCTION

    # check if reproduction counter counts correctly
    assert agent1.reproduction_counter == 1
    assert agent2.reproduction_counter == 1

    # check the attributes of the new agent
    new_agent = board.agents_list[2]
    assert new_agent.parent_A == agent1.number
    assert new_agent.parent_B == agent2.number
    assert new_agent.genetic["Tribe"] == 1

def test_genedistribution_through_heredity():
    parent1 = Agent(1)
    parent2 = Agent(2)
    parent1.genetic = {'Kondition': 2, 'Visibilityrange': 1, 'Tribe': 3, 'Resistance': 2, 'Metabolism': 1, 'Intelligent': True, 'Aggressive': False}
    parent2.genetic = {'Kondition': 1, 'Visibilityrange': 3, 'Tribe': 1, 'Resistance': 3, 'Metabolism': 2, 'Intelligent': False, 'Aggressive': True}
    
    # create child and apply genedistribution_thru_heredity:
    child = Agent(3)
    child.genedistribution_thru_heredity(parent1, parent2)
    
    # check if the "Tribe" gene value is either from parent1 or parent2:
    assert child.genetic['Tribe'] in [parent1.genetic['Tribe'], parent2.genetic['Tribe']]
    
    # check if the "Tribe" values of  child, parent1, parent2 are distinct:
    #assert len(set([child.genetic['Tribe'], parent1.genetic['Tribe'], parent2.genetic['Tribe']])) == 3


# ----------------------   BOARD  ----------------------
def test_board_initialization():
    board = Board(WIDTH, HEIGHT)
    assert board.width == WIDTH
    assert board.height == HEIGHT
    assert len(board.agents_list) == 0
    
    # check if board has correct width and height:
    assert board.width == WIDTH
    assert board.height == HEIGHT
    
    # check if the agents-list is initially empty:
    assert len(board.agents_list) == 0
    
    # check if  food array is initialized with None:
    for row in board.food:
        for cell in row:
            assert cell == 0
    
    # check if world-array is initialized with zeros:
    for row in board.world:
        for cell in row:
            assert cell == 0

def test_board_add_agent():
    board = Board(WIDTH, HEIGHT)
    agent = Agent(1)

    # check if agent was added to the board:
    board.add_agent(agent)
    assert len(board.agents_list) == 1


def test_board_place_food():
    board = Board(WIDTH, HEIGHT)
    board.place_food(FOOD_PERCENTAGE_BEGINNING)
    
    # calc. expected number of food-locations (based on the percentage):
    expected_food_count = int(WIDTH * HEIGHT * FOOD_PERCENTAGE_BEGINNING)
    
    # check actual number of food-locations matches expected number:
    actual_food_count = sum(1 for row in board.food for cell in row if cell is not None)
    assert actual_food_count == expected_food_count
    
    # check if the food is placed randomly on the board:
    unique_food_positions = set((x, y) for x, row in enumerate(board.food) for y, cell in enumerate(row) if cell is not None)
    assert len(unique_food_positions) == actual_food_count


def test_board_remove_agents():
    board = Board(WIDTH, HEIGHT)
    agent = Agent(1)
    board.add_agent(agent)
    board.remove_agents(agent)
    # check if agent was removed successfully
    assert len(board.agents_list) == 0


# ----------------------   GAME  ----------------------
def test_game_initialization():
    # Create a game instance with saving disabled (saving=False) --> not implemented anymore
    # because: ""helps focus the test on the core initialization aspects"""
    # ""without worrying about the actual file writing""
  
    game = Game()
    game.worlds = 1  # Simulate with only one world for simplicity
    assert game.board.width == WIDTH
    assert game.board.height == HEIGHT
    return game

    # check if the board has agents in the agents-list:
    assert len(game.board.agents_list) > 0

    # check if the simulation ran for the expected number of rounds as set:
    assert len(game.board.agents_list) >= 0 and len(game.board.agents_list) <= WIDTH * HEIGHT * ROUNDS

def test_run_simulation_ends_correctly(setup_game):
    game = setup_game
    game.ROUNDS = 2  # Set a small number of rounds for quick testing
    game.NUMBER_AGENTS = 5  # Set a number of agents
    game.FOOD_PERCENTAGE_BEGINNING = 0.1
    game.ADDITIONAL_FOOD_PERCENTAGE = 0.05
    
   # Mock the visualization and agent movement to avoid complex dependencies
    game.visualize_board = lambda: None
    Agent.move = lambda self, board: None
    Agent.reproduce = lambda self, partner, board: None

    game.run()

    assert len(game.data_list) == game.worlds, "Data for each world should be collected"
    # This checks if the game correctly resets agents and food for each new world
    assert not any(game.board.agents_list) and not np.any(game.board.food), "Agents and food should be reset after simulation"
    
def test_game_save_data():
    #game = Game(saving=True) #now enable saving bc it is being tested
    game = Game()
    game.run()
    
    # check if the results-directory and the CSV were created:
    result_dir = f"src/results"
    assert os.path.exists(result_dir)
    csv_file = f"{result_dir}/agent_data_0.csv"
    assert os.path.exists(csv_file)
    
    # check if CSV contains the expected header:
    with open(csv_file, 'r') as file:
        header = file.readline().strip()
        assert header == "Number, Tribe, Condition, Visibility Range, Metabolism, Covered Distance, Reproduction Counter, Consume Counter, Sickness Counter, Parent A, Parent B, Position"
    
    # check if the CSV contains any data rows:
    with open(csv_file, 'r') as file:
        data_lines = file.readlines()[1:]
        assert len(data_lines) > 0
