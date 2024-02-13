import pytest
import numpy as np
from io import StringIO
import sys
from contextlib import redirect_stdout

@pytest.fixture
#Fixtures:  Ressourcen/Daten, die von Tests genutzt werden können
#kann Ressourcen initialisieren/Verbindungen aufbauen/Daten bereitstellen, die von den Tests verwendet werden sollen

def setup_game():
    game = Game()
    return game

def test_lebewesen_creation():
    lebewesen = Lebewesen(1)
    assert lebewesen.nummer == 1
    assert lebewesen.energie == START_ENERGIE
    assert lebewesen.position[0] >= 0 and lebewesen.position[0] < BREITE
    assert lebewesen.position[1] >= 0 and lebewesen.position[1] < HÖHE
    assert lebewesen.fortpflanzungs_counter == 0

def test_genverteilung():
    lebewesen = Lebewesen(1)
    lebewesen.genverteilung()
    assert 'Kondition' in lebewesen.genetik
    assert 'Sichtweite' in lebewesen.genetik
    assert 'Stamm' in lebewesen.genetik

def test_bewegen(setup_game):
    game = setup_game
    lebewesen = game.board.lebewesen[0]
    original_position = lebewesen.position
    lebewesen.bewegen(game.board)
    assert lebewesen.position != original_position or lebewesen.energie < START_ENERGIE

def test_suche_nahrung(setup_game):
    game = setup_game
    lebewesen = game.board.lebewesen[0]
    lebewesen.position = (0, 0)
    game.board.nahrung[0][0] = ENERGIE_NAHRUNG
    lebewesen.suche_nahrung(game.board)
    assert lebewesen.energie > START_ENERGIE

def test_fortpflanzen(setup_game):
    game = setup_game
    lebewesen1 = game.board.lebewesen[0]
    lebewesen2 = game.board.lebewesen[1]
    lebewesen1.fortpflanzen(lebewesen2, game.board)
    assert len(game.board.lebewesen) == ANZAHL_LEBEWESEN + 1
    assert game.board.lebewesen[-1].nummer == lebewesen1.nummer + 1

def test_genverteilung_durch_vererbung():
    lebewesen1 = Lebewesen(1)
    lebewesen2 = Lebewesen(2)
    kind = Lebewesen(3)
    kind.genverteilung_durch_vererbung(lebewesen1, lebewesen2)
    assert 'Kondition' in kind.genetik
    assert 'Sichtweite' in kind.genetik
    assert 'Stamm' in kind.genetik

def test_game_run(setup_game, capsys):
    game = setup_game
    game.run()
    captured = capsys.readouterr()
    assert 'Error' not in captured.out

def test_speichere_daten(setup_game, capsys):
    game = setup_game
    game.run()
    game.speichere_daten()
    captured = capsys.readouterr()
    assert 'Error' not in captured.out
    assert 'lebewesen_daten.csv' in captured.out