#!/usr/bin/env python3

"""tic-tac-toe.py

Tic-Tac-Toe like game.

Copyright (C) 2020 Michael Berry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from copy import deepcopy
from math import inf as infinity
from random import choice
from time import sleep
from typing import Callable, List, Tuple, Union


class Player:
    def __init__(self, symbol: str) -> None:
        """Create a player.
        :param symbol: character used for when str() or print() are called
        :param ai: True if player is AI, else false
        """
        self.symbol = symbol

    def __str__(self) -> str:
        """String representation of Player for print() and str() calls."""
        return self.symbol

    def get_move(self, game):
        """All player types must generate moves."""
        pass


class HumanPlayer(Player):
    def __init__(self, symbol) -> None:
        """Create a human player.
        :param symbol: character that represents the player.
        :return: None
        """
        super().__init__(symbol)
        self.ai = False

    def get_move(self, game) -> Union[bool, Tuple[int, int]]:
        """Get a move from a human player.
        :param game: game state.
        :return: an (x, y) board coordinate, or False if."""
        number = input(f"\n{self.symbol}'s turn, Enter a number: ")
        if (move := game.translate_to_coord(number)):
            return move
        return False


class MiniMax_AI_Player(Player):
    def __init__(self, symbol) -> None:
        """Initialize and AI player.
        :param symbol: character that represents the player.
        :return: None"""
        super().__init__(symbol)
        self.ai = True

    def get_move(self, game) -> Tuple[int, int]:
        """Generate and AI move.
        :param game: game state
        :return: None"""
        if len(game.empty_cells()) == 9:
            move = choice(game.empty_cells())
        else:
            move = self.minimax(game, len(game.empty_cells()), self.symbol)
        return move

    def evaluate(self, state) -> int:
        """Return the score for the current board state.
        :param state: current game state
        :return: 1 if self has won, -1 if other player wins, 0 for a draw
        """
        if self.wins(state, self.symbol):
            score = 1
        elif self.wins(state, "o" if self.symbol == "x" else "x"):
            score = -1
        else:
            score = 0
        return score

    def wins(self, state, player) -> Union[None, List]:
        """Check if game state has a winning move for player.
        :param state: current game state
        :player: current player to check for a win
        :return: None or a list of player value 3 times
        """
        win_state = [
            [state.board[0][0], state.board[0][1], state.board[0][2]],
            [state.board[1][0], state.board[1][1], state.board[1][2]],
            [state.board[2][0], state.board[2][1], state.board[2][2]],
            [state.board[0][0], state.board[1][0], state.board[2][0]],
            [state.board[0][1], state.board[1][1], state.board[2][1]],
            [state.board[0][2], state.board[1][2], state.board[2][2]],
            [state.board[0][0], state.board[1][1], state.board[2][2]],
            [state.board[2][0], state.board[1][1], state.board[0][2]],
        ]
        return [player, player, player] in win_state

    def minimax(self, state, depth, player) -> List:
        """Use the minimax algorithm to determine AI move.
        :param state: current game state
        :param depth: maximum recursion depth
        :param player: current player
        :return: a list where list[0:1] is x,y board coordinates, and list[2] is a score
        """
        if player == self.symbol:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, infinity]

        if depth == 0 or self.wins(state, "x") or self.wins(state, "o"):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in state.empty_cells():
            # Create a copy of the board
            board_copy = deepcopy(state.board)

            # Simulate possible moves
            x, y = cell[0], cell[1]
            state.board[x][y] = player
            score = self.minimax(
                state, depth - 1, "o" if player == "x" else "x")

            # Undo simulation
            state.board = board_copy

            # Determine best score for player
            score[0], score[1] = x, y

            if player == self.symbol:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
        return best


class PlayerSet:
    def __init__(self, player_one, player_two) -> None:
        """Create two players, player One is x, player Two is o.
        Player One starts the game.
        :param:
        """
        self.players = {"One": player_one, "Two": player_two}
        self.active = self.players["One"]

    def switch_player(self) -> None:
        """Switch active player."""
        if self.active == self.players["One"]:
            self.active = self.players["Two"]
        else:
            self.active = self.players["One"]


class TicTacToe:
    def __init__(self) -> None:
        """Create the game board, represented as a 3x3 matrix."""
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.players = game_config()

    def __str__(self) -> str:
        """Display the pretty ascii board."""
        return f"""
        {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}
        ----------
        {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}
        ----------
        {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}"""

    def empty_cells(self) -> Union[None, List]:
        """A list of empty empty cells.
        :return: None, or a list of empty cells
        """
        cells = []
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if str(cell).isdigit():
                    cells.append([x, y])
        return cells

    def valid_move(self, x, y) -> bool:
        """Check if a move is valid.
        :return: True if move is available, else False
        """
        return [x, y] in self.empty_cells()

    def make_move(self, player: Player, move: Tuple[int, int]) -> bool:
        """Mark a move on the board as played.
        :param player: current player
        :param move: valid matrix index
        """
        x, y = move[0], move[1]
        if self.valid_move(x, y):
            self.board[x][y] = str(player)
            return True
        return False

    def translate_to_coord(self, move: str) -> Union[bool, Tuple[int, int]]:
        """Check that a move is a valid play.
        :param move: digit representing index of board matrix
        :return: valid row,col tuple or boolean False
        """
        # Convert move number to a valid coord on game board
        coord_lookup = {
            "1": (0, 0),
            "2": (0, 1),
            "3": (0, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "7": (2, 0),
            "8": (2, 1),
            "9": (2, 2),
        }

        # Return index of coord to symbol
        if move in coord_lookup.keys():
            return coord_lookup[move]

        return False

    def has_winner(self) -> bool:
        """Check for end of game.
        :return: True is game is over
        """
        # Check for horizontal wins
        for row in self.board:
            if row[0] == row[1] == row[2]:
                return True

        # Check for vertical wins
        for col in range(len(self.board[0])):
            vertical = []
            for row in self.board:
                vertical.append(row[col])
            if vertical[0] == vertical[1] == vertical[2]:
                return True

        # Check for diagonal wins
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True

        return False


def catch_keyboard_interrupt(func) -> Callable:
    """Catch keyboard interrupt and exit process.
    :param func: function to wrap around
    :return: wrapper function
    """

    def wrapper(*args, **kwargs) -> Callable:
        """Wrapper around func to catch keyboard interrupt.
        :param args: wrapped function arguments
        :param kwargs: wrapped function keyword arguments
        :return: wrapped function
        """
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nProcess terminated.")
            exit(0)

    return wrapper


def game_config() -> PlayerSet:
    """Configure a PlayerSet, human vs human, human vs computer, etc.
    :return: a configured PlayerSet
    """
    print("Tic-tac-toe\n")
    print("1) Human vs Human")
    print("2) Human vs Computer")
    print("3) Computer vs Human")
    print("4) Computer vs Computer\n")

    # Get game type
    while game_type := input("Game type [1, 2, 3, 4]: "):
        try:
            game_type = int(game_type)
        except ValueError:
            print("\nPlease enter 1, 2, 3, or 4\n")
            continue

        # Setup player set
        if game_type == 1:
            players = PlayerSet(HumanPlayer("x"), HumanPlayer("o"))
            break
        elif game_type == 2:
            players = PlayerSet(HumanPlayer("x"), MiniMax_AI_Player("o"))
            break
        elif game_type == 3:
            players = PlayerSet(MiniMax_AI_Player("x"), HumanPlayer("o"))
            break
        elif game_type == 4:
            players = PlayerSet(MiniMax_AI_Player("x"), MiniMax_AI_Player("o"))
            break
        else:
            print("\nPlease enter 1, 2, 3, or 4\n")

    return players


@catch_keyboard_interrupt
def main() -> None:
    """Main function.
    :return: None
    """
    game = TicTacToe()  # create the game

    print(game)

    # Main loop
    while True:
        print(f"\n{game.players.active}'s turn")

        # Get a move
        if not (move := game.players.active.get_move(game)):
            continue

        # Delay if player is AI
        if game.players.active.ai:
            sleep(0.8)

        # Update the game
        if game.make_move(game.players.active, move):
            print(game)

            # Check for a winner
            if game.has_winner():
                print(f"\nGame over! {game.players.active} wins.")
                exit(0)

            # Check for a draw
            if len(game.empty_cells()) == 0:
                print("\nGame over. Draw.")
                exit(0)

            # Swap whose turn it is
            game.players.switch_player()


# __main__? Program entry point
if __name__ == "__main__":
    main()
