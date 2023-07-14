from game_of_life import GameOfLife

def testEqual(x, y):
    """ Controlla se x e y sono uguali e restituisce 1 se non lo sono e 0 se lo sono"""
    if x == y:
        print("Pass")
        return 0
    else:
        print("Not Passing")
        return 1

def test_game_of_life():
    # Test creazione griglia
    game = GameOfLife(10, 20, 0.5)
    grid = game.create_grid()
    testFalliti = testEqual(len(grid), 10)
    testFalliti += testEqual(len(grid[0]), 10)

    # Test aggiornamento generazione
    game.grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    game.update_generation()
    expected_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    testFalliti += testEqual(game.grid, expected_grid)

    # Test conteggio vicini
    game.grid = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]
    count = game.count_neighbors(1, 1)
    testFalliti += testEqual(count, 4)

    # Aggiungi altri test se necessario

    # Controllo finale
    if testFalliti == 0:
        print("Tutti i test sono passati!")
    else:
        print("Test falliti:", testFalliti)

test_game_of_life()
