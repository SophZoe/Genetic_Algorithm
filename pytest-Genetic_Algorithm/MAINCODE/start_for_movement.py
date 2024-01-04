import numpy as np
#from GenDispense_v01.py import Lebewesen 

class search_for_food():
    range = Lebewesen.wahrnehmungsreichweite
    position = Lebewesen.position
    
    def visible_area(range , position):     #(range = Lebewesen.wahrnehmungsreichweite, position = Lebewesen.position )
        # construncting an array of the size of the agents visible area, with tuples as koordinates
        def viewfield(arr):
            tuples_array = [(val1, val2) for val1 in arr for val2 in arr]
            return tuples_array
        
        # fitting the visible area´s coordinates to the position of the agent
        def fit_to_position(arr, position):
            return [(x + position[0], y + position[1]) for x, y in arr]
        
        
        
        rad = np.linspace(-range, range, range*2+1) 
        """einzelnen integer ausgängig von der reichweite, wenn range = 10,
         dann ist das eine Liste von -10 bis 10"""
        
        #print(rad)
        
        field_to_search = viewfield(rad)
        field_to_search = fit_to_positions(field_to_search, position)
        
        return field_to_search
        
    #area which the agent can overlook 
    field_to_search = visible_area(range, position)
        
    #function to search food in for agent visible area
    def find_food(field_to_search, food_position): #(field_to_search, food_position = Food.position)
        
        for i in field_to_search:
            if i == food_position:
                food_found = True
                break
        else:
            food_found = False
        
    return food_found
    
    #returns True or False for found food
    food_found = find_food(field_to_search, food_position)



