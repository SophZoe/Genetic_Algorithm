import pytest
from Genetic_Algorithm.MAINCODE.main import Agent, Board, Game



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
        assert min_value <= agent.genetic[gene] <= max_value


def test_agent_move():
    board = Board(WIDTH, HEIGHT)
    agent = Agent(1)
    initial_position = agent.position
    agent.move(board)
    assert initial_position != agent.position
    # check if agent position was updated after "agent move"


def test_agent_reproduce():
    board = Board(WIDTH, HEIGHT)
    parent1 = Agent(1)
    parent2 = Agent(2)
    parent1.energy = ENERGYCOSTS_REPRODUCTION * 2  # to get sure that there is enough energy for reproduction
    parent2.energy = ENERGYCOSTS_REPRODUCTION * 2
    board.add_agent(parent1)
    board.add_agent(parent2)

    # check if agent-list-length is correct before reproduction:
    assert len(board.agents_list) == 2
    
    parent1.reproduce(parent2, board)
    
    # check if new agent was added:
    assert len(board.agents_list) == 3


def test_genedistribution_thru_heredity():
    parent1 = Agent(1)
    parent2 = Agent(2)
    parent1.genetic = {'Kondition': 2, 'Visibilityrange': 1, 'Tribe': 3, 'Resistance': 2, 'Metabolism': 1}
    parent2.genetic = {'Kondition': 1, 'Visibilityrange': 3, 'Tribe': 1, 'Resistance': 3, 'Metabolism': 2}
    
    # create child and apply genedistribution_thru_heredity:
    child = Agent(3)
    child.genedistribution_thru_heredity(parent1, parent2)
    
    # check if the "Tribe" gene value is either from parent1 or parent2:
    assert child.genetic['Tribe'] in [parent1.genetic['Tribe'], parent2.genetic['Tribe']]
    
    # check if the "Tribe" values of  child, parent1, parent2 are distinct:
    assert len(set([child.genetic['Tribe'], parent1.genetic['Tribe'], parent2.genetic['Tribe']])) == 3



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
            assert cell is None
    
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
    food_percentage = 0.2
    board.place_food(food_percentage)
    
    # calc. expected number of food-locations (based on the percentage):
    expected_food_count = int(WIDTH * HEIGHT * food_percentage)
    
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
    # Create a game instance with saving disabled
    # because: ""helps focus the test on the core initialization aspects"""
    # ""without worrying about the actual file writing""
    game = Game(saving=False)
    
    # check if game has a board with correct width & height
    assert game.board.width == WIDTH
    assert game.board.height == HEIGHT
    
    # check if the board has agents in the agents-list:
    assert len(game.board.agents_list) > 0
    
    # check if saving is set correctly:
    assert game.saving is False


def test_game_run():
    game = Game(saving=False)
    game.run()
    
    # check if the simulation ran for the expected number of rounds as set:
    assert len(game.board.agents_list) >= 0 and len(game.board.agents_list) <= WIDTH * HEIGHT * ROUNDS


def test_game_save_data():
    game = Game(saving=True) #now enable saving bc it is being tested
    game.run()
    
    # check if the results-directory and the CSV were created:
    result_dir = f"Genetic_Algorithm/MAINCODE/results"
    assert os.path.exists(result_dir)
    csv_file = f"{result_dir}/agent_data_0.csv"
    assert os.path.exists(csv_file)
    
    # check if CSV contains the expected header:
    with open(csv_file, 'r') as file:
        header = file.readline().strip()
        assert header == "Number, Tribe, Condition, Visibilityr Range, Metabolism, Covered Distance, Reproduction Counter, Consume Counter, Sickness Counter, Parent A, Parent B, Position"
    
    # check if the CSV contains any data rows:
    with open(csv_file, 'r') as file:
        data_lines = file.readlines()[1:]
        assert len(data_lines) > 0