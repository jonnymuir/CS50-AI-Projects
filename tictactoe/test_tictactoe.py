import unittest
from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax, X, O, EMPTY

class TestTicTacToe(unittest.TestCase):

    def test_initial_state(self):
        board = initial_state()
        self.assertEqual(board, [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]])

    def test_player(self):
        board = initial_state()
        self.assertEqual(player(board), X)
        board[0][0] = X
        self.assertEqual(player(board), O)

    def test_actions(self):
        board = initial_state()
        self.assertEqual(actions(board), {(i, j) for i in range(3) for j in range(3)})
        board[0][0] = X
        self.assertEqual(actions(board), {(i, j) for i in range(3) for j in range(3) if (i, j) != (0, 0)})

    def test_result(self):
        board = initial_state()
        new_board = result(board, (0, 0))
        self.assertEqual(new_board[0][0], X)
        self.assertEqual(board[0][0], EMPTY)  # Ensure original board is not modified

    def test_winner(self):
        board = [[X, X, X], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[O, EMPTY, EMPTY], [O, EMPTY, EMPTY], [O, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[X, EMPTY, O], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), None)

    def test_terminal(self):
        board = [[X, X, X], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertTrue(terminal(board))
        board = [[O, EMPTY, EMPTY], [O, EMPTY, EMPTY], [O, EMPTY, EMPTY]]
        self.assertTrue(terminal(board))
        board = [[X, EMPTY, O], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]
        self.assertTrue(terminal(board))
        board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertFalse(terminal(board))

    def test_utility(self):
        board = [[X, X, X], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(utility(board), 1)
        board = [[O, EMPTY, EMPTY], [O, EMPTY, EMPTY], [O, EMPTY, EMPTY]]
        self.assertEqual(utility(board), -1)
        board = [[X, EMPTY, O], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]
        self.assertEqual(utility(board), 1)
        board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(utility(board), 0)

    def test_minimax(self):
        board = [[X, O, X], 
                 [X, O, EMPTY], 
                 [O, EMPTY, EMPTY]]
        
        self.assertEqual(minimax(board), (2, 1))  # X should block O's win
        board = [[X, O, O],
                 [O, X, EMPTY], 
                 [X, X, EMPTY]]
        self.assertEqual(minimax(board), (2, 2))  # O should block X's win

if __name__ == '__main__':
    unittest.main()