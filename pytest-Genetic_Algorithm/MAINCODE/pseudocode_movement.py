def Move():
    """
    methoden diw  wir benötigen:
        direction: wie bestimmen wir in wleche richtung der Agent sich bewegen soll
                --> andere Funktion, Gen für Abtastung ob Essen in der Nähe search_food()
        etwas das die position des agenten im array tracked
        
    position = current position in array
               array == "AgentNr.1"   #aktuelle position des agenten abfragen, vermutlich komplizierter, wenn z.b. sich in einem Feld mehrere Agenten und Items befinden können
                                      #im besten falle ein Tupel mit zeile und spalte im array
    def search_food():
        
        #abfragen, was für eine Abtastungsrange ein Agent hat, falls wir dies als Gen implementieren
        search_range = Agent.gene.search_range #sollte ein radius sein, d.h. in alle richtungen kann der Agent so weit schauen
        
        
    field_to_search_in = array[position(0)+search_range:position(1)+search_range, position(0)+search_range:position(1)+search_range] #sowas in der art

    if field_to_search_in != leer:
        food_found = True

    if food_found == True:
        bewegen in die Rcihtung des essen (rechts links oben unten und diagonal)
        rechts = array[position + (1,0)]
        links =  array[position + (-1,0)]
        oben = array[position + (0,-1)]
        unten = array[position + (0,1)]
        diagonal_rechts_oben = .......
        ...
        new_position = array(rechts)
    else:
        possible_directions = [rechts, links, oben, unten, diagonal....]
        --> random aus dieser liste aussuchen z.b. mit index = random.randint(0,8) (wenn 8 richtungen verfügbar)
        new_position = array(rechts)
        

    """
