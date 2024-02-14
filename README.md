<img width="500" height = "300" alt="gen_alg" src="https://github.com/SophZoe/Genetic_Algorithm/assets/128530418/177d348b-8fa6-466a-81f8-b3f121f6f576">

# Dokumentation zum Projekt „Genetische Algorithmen auf Basis von NumPy-Arrays“. 

Aufgabestellung:
https://moodle.hs-duesseldorf.de/pluginfile.php/461132/mod_resource/content/0/Projektauftrag_Genetic_algorithm.pdf


![GitHub repo size](https://img.shields.io/github/repo-size/SophZoe/Genetic_Algorithm) ![GitHub License](https://img.shields.io/github/license/SophZoe/Genetic_Algorithm) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/SophZoe/Genetic_Algorithm/main.yml) ![Python Version](https://img.shields.io/badge/python-3.11%20and%20below-blue)


                                 Nutzer*innen Dokumentation & Developer Dokumentation

1. Systemanforderungen

- Python 3.3 und höher
- NumPy-Bibliothek
- Matplotlib-Bibliothek
- Numba-Bibliothek (optional für Performance-Optimierung)

2. Installation
Stellen Sie sicher, dass Python und die erforderlichen Bibliotheken auf Ihrem System installiert sind. Sie können sie mit pip installieren:
pip install numpy
pip install matplotlib
pip install numba

3. Erklärung des Spiel-Konzepts: 
Dieses Simulationsspiel modelliert das Verhalten von Agenten (Lebewesen) in einer virtuellen Welt. Jeder Agent verfügt über Energie, eine genetische Ausstattung, kann sich bewegen, Nahrung konsumieren, wodurch ihr Energyscore erhöhrt wird, und sich fortpflanzen. Die Welt ist als ein zweidimensionales Feld (Default 100x100) organisiert, auf dem Nahrung zufällig platziert wird. Die Simulation durchläuft mehrere Runden, in denen Agenten agieren, bis sie entweder sterben oder die maximale Anzahl von Runden erreicht wird. Eine Simulation des Fortpflanzungsprozesses basiert sich auf der Berechnung von Energiekosten, berücksichtigt werden außerdem die Erfolgswahrscheinlichkeit auf der Grundlage der Stammeszugehörigkeit und die Übertragung genetischer Merkmale von den Eltern auf den Nachwuchs (Tribes), was zu einer Vielzahl und Dynamik an Agenten führt.


3.1 
Starten der Simulation
Um die Simulation zu starten, muss der Python-Code ausgeführt werden. Der Code initialisiert automatisch eine Spielinstanz und führt die Simulation mit den voreingestellten Parametern durch.

3.2 
Ende der Simulation
Am Ende der Simulation wird die Ausführungszeit in Sekunden ausgegeben. Wenn das Speichern aktiviert ist, werden die Daten der Agenten in einer CSV-Datei im Ordner „results“ gespeichert. Die Datei enthält Informationen zu jedem Agenten, einschließlich Stammeszugehörigkeit, Kondition, Sichtweite, Reproduktionszähler, Konsumzähler, Position und Lebensspanne.

4. Konstanten und Einstellungen
Die Simulation verwendet eine Reihe von Konstanten, um das Verhalten und die Umgebung der Agenten zu definieren:

ENERGYCOSTS_MOVEMENT: Die Energiekosten für die Bewegung eines Agenten.
ENERGYCOSTS_REPRODUCTION: Die Energiekosten für die Fortpflanzung.
START_ENERGY: Die Startenergie eines Agenten.
WIDTH, HEIGHT: Die Dimensionen des Boardes.
NUMBER_AGENTS: Die anfängliche Anzahl der Agenten.
ROUNDS: Die Anzahl der Simulationsrunden.
ENERGY_FOOD: Die Energiemenge, die die verzehrte Nahrung liefert.
FOOD_PERCENTAGE_BEGINNING: Prozentualer Anteil der zufällig plazierten Nahrung am Anfang der Simulation. 
ADDITIONAL_FOOD_PERCENTAGE: Die Menge der zusätzlichen Nahrung (in Prozentsatz), die in jeder neuen Runde hinzugefügt wird.


                    Entwickler*innen Dokumentation

5. Code-Struktur
Der Code besteht aus mehreren Klassen, die die Agenten, das Spielbrett und das Spiel selbst modellieren. Die wichtigsten Klassen sind:
•	Agent: Repräsentiert einen einzelnen Agenten mit den Eigenschaften Energie, genetischen Merkmalen und Position. Methoden dieser Klasse ermöglichen es dem Agenten, sich zu bewegen, Nahrung zu konsumieren und sich fortzupflanzen.
•	Board: Verwaltet das Spielbrett, einschließlich der Position von Nahrung und Agenten. Es ermöglicht das Hinzufügen von Nahrung und das Entfernen von Agenten.
•	Game: Koordiniert den Simulationsablauf, einschließlich der Initialisierung des Spielbretts, dem Hinzufügen von Agenten und der Durchführung von Runden.

5.1 
Wichtige Methoden jeder Klasse und ihre Funktionen

•	Agent
Die Agent-Klasse repräsentiert ein einzelnes Lebewesen im Ökosystem mit folgenden Eigenschaften und Methoden:

- __init__(): Initialisiert einen neuen Agenten mit einer einzigartigen Nummer, Startenergie, zufälliger Position und leerem genetischen Profil.
- genedistribution(): Weist dem Agenten genetische Eigenschaften aus dem GENPOOL zu.
- move(): Bewegt den Agenten und verbraucht Energie, aktualisiert die Position des Agenten.
- search_food(): Sucht in der Nähe des Agenten nach Nahrung. Wenn Nahrung in Reichweite ist, konsumiert der Agent diese.
- reproduce(): Ermöglicht die Fortpflanzung zwischen zwei Agenten, wenn sie sich auf dem gleichen Feld befinden und genügend Energie haben.
- genedistribution_thru_heredity(): Bestimmt die genetischen Eigenschaften eines neugeborenen Agenten basierend auf den Genen der Eltern.

• Board
Die Board-Klasse verwaltet die simulierte Welt, in der die Agenten leben:

__init__(): Initialisiert das Spielbrett, eine Liste für Agenten und einen Zero-NumPy-Array für die Nahrungsverteilung.
add_agent(): Fügt einen neuen Agenten zur Welt hinzu.
place_food(): Platziert Nahrung auf dem Spielbrett basierend auf einem angegebenen Prozentsatz der Felder
place_agents(): Platziert Agenten auf dem Spielbrett für die Visualisierung.
remove_agents(): Entfernt einen Agenten aus dem Spielbrett.

• Game
Die Game-Klasse steuert den Simulationsablauf:
- __init__(): Initialisiert das Spiel auf dem Spielbrett und fügt Agenten und Nahrung hinzu.
- run(): Führt die festgelegte Anzahl der Simulationsrunden aus, in denen Agenten sich zufällig bewegen. Koordiniert die Fortpflanzung und die Suche nach Nahrung.
- safe_data(): Speichert die Simulationsdaten in einer CSV-Datei.
- visualize_board(): Visualisiert die Welt und die Verteilung von Agenten und Nahrung.

6. Anpassung und Erweiterung
Der Code kann in seiner Struktur dynamisch erweitert und verändert werden. Vor allem die anfangs festgelegte Konstanten lassen sich entsprechend der Bedingungen einer neuen Welt angepassen. Mögliche Anpassungen umfassen:
- die Änderung der Energiekosten für Bewegungen und Fortpflanzung,
- Verhalten der Agenten (eventuell Einfürung die Agenten, die sich agressiv gegenüber den anderen Agenten verhalten,
- Dynamik der Simulation (das Spielbrett könnte skaliert werden, um die Ausführungszeit für die Runden zu beschleunigen,
- die Einführung neuer genetischer Merkmale,
-  die Anpassung der Wahrscheinlichkeiten für Krankheiten.

7. Speichern und Auswerten von Daten
Die Option zum Speichern der Simulationsergebnisse in einer CSV-Datei ermöglicht die nachträgliche Analyse und Auswertung der Simulationsläufe, um zusätzliche Erkenntnisse zu gewinnen im Hinblick auf Verbesserungsmöglichkeiten/Erweiterungen der Simulation oder datentechnische Analysen durchzuführen.

8. Tests und Maßnahmen für die Continuous Integration des Codes
  
8.1 
Allgemeine Hinweise zur Ausführung der Tests: 
Installieren Sie pytest und stellen Sie sicher, dass alle erforderlichen Bibliotheken installiert sind.
Führen Sie die Tests mit dem pytest-Befehl in Ihrem Terminal oder einer integrierten Entwicklungsumgebung (IDE) aus.
Überprüfen Sie die Ausgabe auf Fehler und stellen Sie sicher, dass alle Tests bestanden werden, um die Integrität des Simulationscodes zu gewährleisten.
Die Tests sind so konzipiert, dass sie die Kernfunktionalität des Simulationscodes abdecken und sicherstellen, dass die Grundlogik der Agentenbewegungen, der Nahrungsaufnahme, der Fortpflanzung und der Vererbung wie beabsichtigt funktioniert. 

8.2 
Testfälle:
- test_add_agent
Beschreibung: Überprüft, ob ein Agent (Lebewesen) korrekt mit den vorgesehenen Startwerten initialisiert wird.
Zweck: Stellt sicher, dass die Agenten mit der korrekten Nummer, Startenergie und einer gültigen Anfangsposition innerhalb der Spielgrenzen erstellt werden und dass der Fortpflanzungs-Counter auf 0 gesetzt ist.

- test_genedistribution 
Beschreibung: Testet die genverteilung-Methode eines Agenten.
Zweck: Bestätigt, dass die Gene des Agenten aus dem GENPOOL korrekt zugewiesen werden, indem überprüft wird, ob die Schlüsselwörter im genetik-Dictionary des Agenten vorhanden sind.

- test_move
Beschreibung: Überprüft die bewegen-Methode eines Agenten.
Zweck: Prüft, ob der Agent sich bewegt (indem er die Position ändert) oder ob die Energie des Agenten nach dem Versuch, sich zu bewegen, abnimmt, falls keine Bewegung stattfindet.

- test_search_food
Beschreibung: Testet, ob ein Agent Nahrung auf dem Spielbrett erfolgreich suchen und seine Energie erhöhen kann.
Zweck: Bestätigt, dass die suche_nahrung-Methode die Energie des Agenten erhöht, wenn sich Nahrung an seiner Position befindet.

- test_reproduction
Beschreibung: Überprüft die fortpflanzen-Methode zwischen zwei Agenten.
Zweck: Stellt sicher, dass nach dem Aufruf der Methode ein neues Agenten-Objekt der Agentenliste des Spielbretts hinzugefügt wird und dass sich die nummer des neuen Agenten korrekt erhöht.

- test_gen_distribution_through_inheritance
Beschreibung: Testet die Vererbung von Genen in der genverteilung_durch_vererbung-Methode.
Zweck: Überprüft, ob die Gene der Nachkommen korrekt aus den Genen der Eltern kombiniert werden.

- test_run
Beschreibung: Testet die run-Methode des Spiels.
Zweck: Validiert, dass das Spiel ohne Fehler ausgeführt wird und die Simulationsrunden durchläuft.

- test_save_data
Beschreibung: Testet die speichere_daten-Methode des Spiels.
Zweck: Bestätigt, dass die Simulationsergebnisse korrekt in eine CSV-Datei geschrieben werden können.

---------------------------------------------------------------------------------------------------------------------------------------
ENG: 
Documentation for the project "Genetic algorithms based on NumPy arrays". 

Assignment Description:
https://moodle.hs-duesseldorf.de/pluginfile.php/461132/mod_resource/content/0/Projektauftrag_Genetic_algorithm.pdf


                                 User documentation & developer documentation

1. System Requirements

- Python 3.3 and above
- NumPy Module
- Matplotlib Library
- Numba Library (optional for performance optimization)

2. Installation
Make sure that Python and the required libraries are installed on your system. You can install them using the pip:
pip install numpy
pip install matplotlib
pip install numba

3. Game Concept
This simulation game mreproduce the behavior of agents (living beings) in a virtual world. Each agent has energy, genetic inheritance features, can move, consumes food, which increases their energy score, and reproduce. The world is organized as a two-dimensional field (default 100x100) on which food is randomly placed. The simulation runs through several rounds (up to 100) in which agents act until they either die or the maximum number of rounds is reached. Reproduction works as follows:
firstly the  energy costs will be accounted, secondly the success rate based on strain affiliation is to be added, and the transfer (inheritance) of genetic traits from parents to offspring takes place, resulting in a diverse and dynamic population of agents over time.

3.1 
Starting the simulation
To start the simulation, the Python code must be executed. The code automatically initializes a game instance and runs the simulation with the preset parameters.

3.2 
End of the simulation
At the end of the simulation, the execution time is displayed in seconds. If saving is activated, the agent data is saved in a CSV file in the "results" folder. The file contains information on each agent, including strain affiliation, condition, visibility, reproduction counter, consumption counter, position and lifespan.

4 Constants and settings
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


                    Developer documentation

5. code structure
The code consists of several classes that model the agents, the game board and the game itself. The most important classes are:
- Agent: Represents a single agent with the properties energy, genetic traits and position. Methods of this class allow the agent to move, consume food and reproduce.
- Board: Manages the game board, including the position of food and agents. It allows the addition of food and the removal of agents.
- Game: Coordinates the simulation process, including initializing the game board, adding agents and conducting rounds.

5.1 
Important methods of each class and their functions

- Agent
The Agent class represents a single living being in the ecosystem with the following properties and methods:

- __init__(): Initializes a new agent with a unique number, starting energy, random position and empty genetic profile.
- genedistribution(): Assigns genetic properties from the GENPOOL to the agent.
- move(): Moves the agent and consumes energy, updates the position of the agent.
- search_food(): Searches for food near the agent. If food is within reach, the agent consumes it.
- reproduce(): Enables reproduction between two agents if they are on the same field and have enough energy.
- genedistribution_thru_heredity(): Determines the genetic traits of a newborn agent based on the parents' genes.

- Board
The board class manages the simulated world in which the agents live:

__init__(): Initializes the game board, a list for agents and a Zero-NumPy array for food distribution.
add_agent(): Adds a new agent to the world.
place_food(): Places food on the board based on a specified percentage of spaces
place_agents(): Places agents on the game board for the further visualization.
remove_agents(): Removes an agent from the game board.

- Game
The Game class controls the simulation process:
- __init__(): Initializes the game on the game board and adds agents and food.
- run(): Runs the specified number of simulation rounds in which agents move randomly. Coordinates reproduction and the search for food.
- safe_data(): Saves the simulation data in a CSV file.
- visualize_board(): Visualizes the world and the distribution of agents and food.

6. Customization and possible feature extension
The structure of the code can be extended and changed dynamically. In particular, the initially defined constants can be adapted according to the conditions of a new world. Possible adaptations include
- Changing the energy costs for movement and reproduction,
- Agent behavior (possibly introducing agents that behave aggressively towards other agents,
- dynamics of the simulation (the game board could be scaled to speed up the execution time for the rounds,
- the introduction of new genetic traits,
- the adjustment of probabilities for diseases.

7. Saving and analyzing the generated data
The option to save the simulation results in a CSV file enables the subsequent analysis and evaluation of the simulation runs in order to gain additional insights with regard to possible improvements/extensions of the simulation or to carry out data-related analyses.

8. Tests and measures for the continuous integration of the code
  
8.1 
General instructions for running the tests: 
Install pytest and make sure that all required libraries are installed.
Execute the tests with the pytest command in your terminal or integrated development environment (IDE).
Check the output for errors and make sure that all tests pass to ensure the integrity of the simulation code.
The tests are designed to cover the core functionality of the simulation code and ensure that the basic logic of agent movement, feeding, reproduction and inheritance works as intended. 

8.2 
Test cases:
- test_add_agent
Description: Checks whether an agent (living being) is initialized correctly with the intended start values.
Purpose: Ensures that the agents are created with the correct number, starting energy and a valid starting position within the game limits and that the propagation counter is set to 0.

- test_genedistribution 
Description: Tests the gene distribution method of an agent.
Purpose: Confirms that the agent's genes are correctly assigned from the GENPOOL by checking that the keywords are present in the agent's genetics dictionary.

- test_move
Description: Checks the move method of an agent.
Purpose: Checks whether the agent moves (by changing position) or whether the agent's energy decreases after attempting to move if no movement occurs.

- test_search_food
Description: Tests whether an agent can successfully search for food on the board and increase its energy.
Purpose: Confirms that the search_food method increases the agent's energy if there is food at its position.

- test_reproduction
Description: Checks the reproduce method between two agents.
Purpose: Ensures that a new agent object is added to the agent list of the game board after the method is called and that the number of the new agent increases correctly.

- test_gen_distribution_through_inheritance
Description: Tests the inheritance of genes in the gene_distribution_through_inheritance method.
Purpose: Checks whether the genes of the offspring are correctly combined from the genes of the parents.

- test_run
Description: Tests the run method of the game.
Purpose: Validates that the game is executed without errors and runs through the simulation rounds.

- test_save_data
Description: Tests the save_data method of the game.
Purpose: Validates that the simulation results can be correctly written to a CSV file and that no errors occur.






