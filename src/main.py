import numpy as np
import time

# Constants
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 10
WIDTH = 10
HEIGHT = 10
NUMBER_AGENTS = 10
ROUNDS = 10
FOOD_PERCENTAGE_BEGINNING = 0
ADDITIONAL_FOOD_PERCENTAGE = 0.01
SICKNESS_DURATION = ROUNDS // 10

VISUALIZE_POISON = True # other option is False

# Global counter for the numbering of living beings EDIT: moved to CLASS_Agent.py
# agents_counter = NUMBER_AGENTS

FOOD = {
    1.0: {'Energy': 5, 'consumption_time': 2, 'disease_risk': 0},
    2.0: {'Energy': 10, 'consumption_time': 6, 'disease_risk': 0},
    3.0: {'Energy': 15, 'consumption_time': 6, 'disease_risk': 0},
    4.0: {'Energy': 20, 'consumption_time': 8, 'disease_risk': 3},
    5.0: {'Energy': 5, 'consumption_time': 2, 'disease_risk': 6},
    6.0: {'Energy': 10, 'consumption_time': 4, 'disease_risk': 9},
    7.0: {'Energy': 15, 'consumption_time': 6, 'disease_risk': 12}
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

# --------------------- MAIN ---------------------

if __name__ == "__main__":

    from package.CLASS_Game import Game     #importing here to avoid circular method-calling
    start = time.time()
    game = Game(saving=True, worlds=1, ROUNDS=5)
    game.run()
    script_time = np.round(time.time() - start, 2)
    print(f"Script time: {script_time}s")
