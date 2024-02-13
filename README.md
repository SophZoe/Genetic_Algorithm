# Dokumentation zum Projekt „Genetische Algorithmen auf Basis von NumPy-Arrays“. 

Aufgabestellung:
https://moodle.hs-duesseldorf.de/pluginfile.php/461132/mod_resource/content/0/Projektauftrag_Genetic_algorithm.pdf


                                                            # Nutzer*innen Dokumentation & Developer Dokumentation

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
Dieses Simulationsspiel modelliert das Verhalten von Agenten (Lebewesen) in einer virtuellen Welt. Jeder Agent verfügt über Energie, eine genetische Ausstattung, kann sich bewegen, Nahrung konsumieren, wodurch ihr Energyscore erhöhrt wird, und sich fortpflanzen. Die Welt ist als ein zweidimensionales Feld (Default 100x100) organisiert, auf dem Nahrung zufällig platziert wird. Die Simulation durchläuft mehrere Runden, in denen Agenten agieren, bis sie entweder sterben oder die maximale Anzahl von Runden erreicht wird. Die Fprtpflanzung finktioniert wie folg:

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
Zweck: Bestätigt, dass die Simulationsergebnisse korrekt in eine CSV-Datei geschrieben werden können und ke





