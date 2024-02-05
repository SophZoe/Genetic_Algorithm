# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 19:50:15 2024

@author: marko
"""
from start_for_movement import food_search.visible_area
import random 

class movement():
    speed = Lebewesen.speed
    position = Lebewesen.position
    
    def steps_per_iter():
        for steps in range(speed):
            position = moving()
            
    def moving(position):
        
        #creating koordintaes (1,1) to (-1,-1) for direction in which to move
        directions = np.linspace(-range, range, range*2+1)
        
        #making an array with tuples (koordinates) which are all the possible directions for moving
        # 9 directions in total (with direction (0,0) as not moving)
        array_directions = food_search.visible_area(directions)
        
        #durch random index eine richtung aussuchen in der sich der agent bewegen soll
        idx = random.randint(0, 8) 
        chosen_direction = array_directions[idx]
        
        #addieren der position und richtung
        new_position = tuple(map(sum, zip(position, chosen_direction))) 
        
        return new_position
        
        
            
    
    """ damit auch leebewesen in einer iteration anhängig von der geschwindigkeit
    bewegen wäre es am besten die bewegung mit schkeifen durchzuführen.
    wie oft die schleife wiederholt wird hängt von speed-wert ab und in jeder iteration der schleife wird
    sich nur ein feld weit bewegt, damit keine felder übersorungen werden
    
    
    
    
    eventuell auch eine startrichtung angeben, damit sicch die agenten niht nur im kreis bewegen solagen diese
    in der iteration kein ziel haben auf die sie sich hinzubewgen"""

#%% funktionierende variante!!!!!
import numpy as np
import random
speed = 5
position =(1,1)

def visible_area(position = position, range = 1):     #(range = Lebewesen.wahrnehmungsreichweite, position = Lebewesen.position )
    def array_to_tuples(arr):
        tuples_array = [(val1, val2) for val1 in arr for val2 in arr]
        #print(f"tuples_array {tuples_array}")
        return tuples_array
    """
    #anpassen der sichtabren felder an position des agentens
    def add_tuples(arr, position):
        return [(x + position[0], y + position[1]) for x, y in arr]
"""
    
    rad = np.linspace(-1, 1, 1*2+1) 
    """einzelnen integer ausgängig von der reichweite, wenn range = 10,
    dann ist das eine Liste von -10 bis 10"""
    
    #print(rad)
    
    field_to_search = array_to_tuples(rad)
   # field_to_search = add_tuples(field_to_search, position)
    #print(f" add tuples:  {field_to_search}")
    return field_to_search

    
def steps_per_iter(speed):
    for steps in range(speed):
        if steps == 0:
            new_position = moving()
            print(f"new:{new_position}\n")
        else:
            new_position = moving(new_position)
            print(f"new:{new_position}\n")
        
def moving(position = position):
    
    #creating koordintaes (1,1) to (-1,-1) for direction in which to move
    directions = np.linspace(-1, 1, 1*2+1)
    
    
    #making an array with tuples (koordinates) which are all the possible directions for moving
    # 9 directions in total (with direction (0,0) as not moving)
    array_directions = visible_area()
    #print(f"directions: {array_directions}")
    
    #durch random index eine richtung aussuchen in der sich der agent bewegen soll
    idx = random.randint(0, 8) 
    chosen_direction = array_directions[idx]
    print(f"chosen direction: {chosen_direction}")
    
    #addieren der position und richtung
    print(f"position: {position}")
    
    new_position = tuple(map(sum, zip(position, chosen_direction))) 
    
    return new_position


steps_per_iter(speed)