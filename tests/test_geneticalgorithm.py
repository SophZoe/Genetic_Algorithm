import pytest
from src.package.class_agent import Agent
from src.package.class_aame import Game
from src.package.class_board import Board
from src.main import GENPOOL, START_ENERGY, WIDTH, HEIGHT, ENERGYCOSTS_REPRODUCTION, ROUNDS, FOOD_PERCENTAGE_BEGINNING
import os

# ----------------------   AGENT  ----------------------
def test_agent_initialization():
    agent = Agent(1)
    assert agent.number == 1
    assert agent.energy == START_ENERGY
    assert agent.sick is False
    # more checks for more attributes


def test_agent_genedistribution():
    agent = Agent(1)
    agent.genedistribution()
    # check if gene-values are within expected range:
    for gene, (min_value, max_value) in GENPOOL["Genes"].items():
        assert min_value <= agent.genetic[gene] <= max_value or isinstance(agent.genetic[gene], bool)


def test_agent_move():
    board = Board(WIDTH, HEIGHT)
    agent = Agent(1)
    initial_position = agent.position
    agent.move(board)
    assert initial_position != agent.position
    # check if agent position was updated after "agent move"


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


def test_genedistribution_thru_heredity():
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
    
    board = Board(WIDTH, HEIGHT)
    
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
    # game = Game(saving=False)
    
    game = Game()

    # check if game has a board with correct width & height
    assert game.board.width == WIDTH
    assert game.board.height == HEIGHT
    
    # check if the board has agents in the agents-list:
    assert len(game.board.agents_list) > 0
    
    # check if saving is set correctly:
    # assert game.saving is False


def test_game_run():
    #game = Game(saving=False)
    game = Game()
    game.run()
    
    # check if the simulation ran for the expected number of rounds as set:
    assert len(game.board.agents_list) >= 0 and len(game.board.agents_list) <= WIDTH * HEIGHT * ROUNDS


def test_game_save_data():
    #game = Game(saving=True) #now enable saving bc it is being tested
    game = Game()
    game.run()
    
    # check if the results-directory and the CSV were created:
    result_dir = f"MAINCODE/results"
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
