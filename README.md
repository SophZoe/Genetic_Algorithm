# Genetic_Algorithm
A study/portfolio case for university https://moodle.hs-duesseldorf.de/pluginfile.php/461132/mod_resource/content/0/Projektauftrag_Genetic_algorithm.pdf



# Nutzer*innen Dokumentation & Developer Dokumentation

## Nutzer*innen Dokumentation

Dieses Simulationsspiel modelliert das Verhalten von Agenten (Lebewesen) in einer virtuellen Welt. Jeder Agent verfügt über Energie, eine genetische Ausstattung, kann sich bewegen, Nahrung konsumieren und sich fortpflanzen. Die Welt ist als ein zweidimensionales Feld organisiert, auf dem Nahrung zufällig platziert wird. Die Simulation durchläuft mehrere Runden, in denen Agenten agieren, bis sie entweder sterben oder die maximale Anzahl von Runden erreicht wird.

### Starten der Simulation
Um die Simulation zu starten, muss der Python-Code ausgeführt werden. Der Code initialisiert automatisch eine Spielinstanz und führt die Simulation mit den voreingestellten Parametern durch.

### Anpassungen
Nutzer*innen können verschiedene Parameter der Simulation anpassen, bevor sie gestartet wird. Diese Anpassungen beinhalten:

•	Die Anzahl der Agenten, die zu Beginn der Simulation platziert werden (NUMBER_AGENTS)
•	Die Anzahl der Runden (ROUNDS), die die Simulation durchlaufen soll
•	Den Prozentsatz der Felder, die zu Beginn zufällig mit Nahrung belegt werden (FOOD_PERCENTAGE_BEGINNING)
•	Die Menge der Nahrung, die in jeder Runde hinzugefügt wird (ADDITIONAL_FOOD_PERCENTAGE)

### Ende der Simulation
Am Ende der Simulation wird die Ausführungszeit in Sekunden ausgegeben. Wenn das Speichern aktiviert ist, werden die Daten der Agenten in einer CSV-Datei im Ordner „results“ gespeichert. Die Datei enthält Informationen zu jedem Agenten, einschließlich Stammeszugehörigkeit, Kondition, Sichtweite, Reproduktionszähler, Konsumzähler, Position und Lebensspanne.

## Entwickler*innen Dokumentation

### Code-Struktur
Der Code besteht aus mehreren Klassen, die die Agenten, das Spielbrett und das Spiel selbst modellieren. Die wichtigsten Klassen sind:
•	Agent: Repräsentiert einen einzelnen Agenten mit den Eigenschaften Energie, genetischen Merkmalen und Position. Methoden dieser Klasse ermöglichen es dem Agenten, sich zu bewegen, Nahrung zu konsumieren und sich fortzupflanzen.
•	Board: Verwaltet das Spielbrett, einschließlich der Position von Nahrung und Agenten. Es ermöglicht das Hinzufügen von Nahrung und das Entfernen von Agenten.
•	Game: Koordiniert den Simulationsablauf, einschließlich der Initialisierung des Spielbretts, dem Hinzufügen von Agenten und der Durchführung von Runden.

### Wichtige Methoden jeder Klasse und ihre Funktionen

#### Agent
•	Agent.move(): Bewegt den Agenten und verbraucht Energie. Wenn Nahrung in Reichweite ist, konsumiert der Agent diese
•	Agent.reproduce(): Ermöglicht die Fortpflanzung zwischen zwei Agenten, wenn sie sich auf dem gleichen Feld befinden und genügend Energie haben

#### Board
•	Board.place_food(): Platziert Nahrung auf dem Spielbrett basierend auf einem angegebenen Prozentsatz der Felder

#### Game
•	Game.run(): Führt die Simulation durch, indem es für eine festgelegte Anzahl von Runden die Aktionen der Agenten steuert und das Hinzufügen von Nahrung koordiniert

### Anpassung und Erweiterung
Der Code kann in seiner Struktur dynamisch erweitert und verändert werden, um das Verhalten der Agenten, die Regeln der Umwelt oder die Dynamik der Simulation zu ändern. Mögliche Anpassungen umfassen die Änderung der Energiekosten für Bewegungen und Fortpflanzung, die Einführung neuer genetischer Merkmale oder die Anpassung der Wahrscheinlichkeiten für Krankheiten.

### Speichern und Auswerten von Daten
Die Option zum Speichern der Simulationsergebnisse in einer CSV-Datei ermöglicht die nachträgliche Analyse und Auswertung der Simulationsläufe, um zusätzliche Erkenntnisse zu gewinnen im Hinblick auf Verbesserungsmöglichkeiten/Erweiterungen der Simulation oder datentechnische Analysen durchzuführen.




