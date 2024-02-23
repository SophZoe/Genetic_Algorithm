"""
Genetic Algorithm - main.py

This module contains set constants and dictionaries\n
which are used by other modules to execute the\n
simulation correctly.\n
Game loop is started from here.

External Dependencies
--------------------
numpy
    numerical operations
    data management
time
    tracks execution time

Authors
-------
    - [@julietteyek] (https://github.com/julietteyek)
    - [@Jxshyz] (https://github.com/Jxshyz)
    - [@Markomrnkvc] (https://github.com/Markomrnkvc)
    - [@SophZoe] (https://github.com/SophZoe)
    - [@Salt-is-leaving] (https://github.com/Salt-is-leaving)

"""
import time
import numpy as np



# Constants
ENERGYCOSTS_MOVEMENT = 1
ENERGYCOSTS_REPRODUCTION = 5
START_ENERGY = 25
WIDTH = 50
HEIGHT = 50
NUMBER_AGENTS = 20
ROUNDS = 20
FOOD_PERCENTAGE_BEGINNING = 0
ADDITIONAL_FOOD_PERCENTAGE = 0.01
SICKNESS_DURATION = ROUNDS // 10

VISUALIZE_POISON = True #other option is False


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
        "Condition": (1, 3),
        "Visibilityrange": (1, 3),
        "Tribe": (1, 3),
        "Resistance": (1, 3),
        "Metabolism": (1, 3),
        "Intelligent": [True, False],
        "Aggressive": [True, False]
    }
}

# --------------------- MAIN ---------------------

def main():
    """
    main
    """
    from class_game import Game     #importing here to avoid circular method-calling
    start = time.time()
    game = Game(saving=True, worlds=1, ROUNDS=5)
    game.run()
    script_time = np.round(time.time() - start, 2)
    print(f"Script time: {script_time}s")

if __name__ == "__main__":
    main()

"""if __name__ == "__main__":

    from package.CLASS_Game import Game     #importing here to avoid circular method-calling
    start = time.time()
    #game = Game(saving=True, worlds=1, ROUNDS=5)
    #game.run()
    app = paramAd(paramAd.initial_parameters, paramAd.run_simulation)
    app.mainloop()
    script_time = np.round(time.time() - start, 2)
    print(f"Script time: {script_time}s")"""
