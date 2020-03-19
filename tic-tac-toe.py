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


import time
import random

from typing import Callable, Tuple, Union


class Player:
    def __init__(self, mark: str) -> None:
        """Create a player.
        :param mark: String used for when str() or print() are called
        """
        self.mark = mark
        self.ai = False  # true if player is computer

    def __str__(self) -> str:
        """String representation of Player for print() and str() calls."""
        return self.mark


class PlayerSet:
    def __init__(self) -> None:
        """Create two players, player One is x, player Two is o.
        Player One starts the game.
        """
        self.players = {"One": Player("x"), "Two": Player("o")}
        self.active = self.players["One"]

    def switch_player(self) -> None:
        """Switch active player."""
        if self.active == self.players["One"]:
            self.active = self.players["Two"]
        else:
            self.active = self.players["One"]


class GameBoard:
    def __init__(self) -> None:
        """Create the logic game board, represented as a 3x3 matrix."""
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.moves = [n for n in range(1, 10)]

    def __str__(self) -> str:
        """Display the pretty ascii board."""
        return f"""
        {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}
        ----------
        {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}
        ----------
        {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}"""

    def mark(self, player: Player, move: Tuple[int, int]) -> None:
        """Mark a move on the board as played.
        :param player: current player
        :param move: valid matrix index
        """
        row, col = move
        self.board[row][col] = str(player)

    def validate_move(self, move: int) -> Union[bool, Tuple[int, int]]:
        """Check that a move is a valid play.
        :param move: int representing index of board matrix
        :return: valid row,col tuple or boolean False
        """
        # Move number should be from 1 to 9
        if move not in range(1, 10):
            print("Invalid move, enter 1-9")
            return False

        # Convert move number to a valid cell on game board
        cell_lookup = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (1, 0),
            5: (1, 1),
            6: (1, 2),
            7: (2, 0),
            8: (2, 1),
            9: (2, 2),
        }

        if move in cell_lookup.keys():
            cell = cell_lookup[move]

        # Check if move has already been played
        if move not in self.moves:
            print("\nMove already taken")
            return False

        # Remove move from available moves
        self.moves.remove(move)

        # Return index of cell to mark
        return cell

    def check_winner(self) -> Union[None, str]:
        """Check for wins.
        :return: None or the winning player
        """
        winner = None

        # Check for horizontal wins
        for row in self.board:
            if row[0] == row[1] == row[2]:
                winner = row[0]

        # Check for vertical wins
        for col in range(len(self.board[0])):
            vertical = []
            for row in self.board:
                vertical.append(row[col])
            if vertical[0] == vertical[1] == vertical[2]:
                winner = vertical[0]

        # Check for diagonal wins
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            winner = self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            winner = self.board[2][0]

        return winner

    def get_move(self, player: Player) -> Union[bool, int]:
        """Get a move from a player.
        :param player: player whose turn it is
        :return: False or number representing a game board move
        """
        number = input(f"\n{player}'s turn, Enter a number: ")
        try:
            move = self.validate_move(int(number))
        except ValueError:
            print("Invalid input, try again.")
            return False

        return move

    def generate_move(self) -> int:
        """Generate a move for computer's turn.
        :return: Number representing a game board move
        """
        random_move = random.choice(self.moves)
        move = self.validate_move(random_move)

        return move


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
    players = PlayerSet()

    print("Tic-tac-toe\n")
    print("1) Human vs Human")
    print("2) Human vs Computer")
    print("3) Computer vs Human")
    print("4) Computer vs Computer\n")

    while game_type := input("Game type [1, 2, 3, 4]: "):
        try:
            game_type = int(game_type)
        except ValueError:
            print("\nPlease enter 1, 2, 3, or 4\n")
            continue

        # Return true of false
        if game_type == 1:
            break
        elif game_type == 2:
            players.players["Two"].ai = True
            break
        elif game_type == 3:
            players.players["One"].ai = True
            break
        elif game_type == 4:
            players.players["One"].ai = True
            players.players["Two"].ai = True
            break
        else:
            print("\nPlease enter 1, 2, 3, or 4\n")

    return players


@catch_keyboard_interrupt
def main() -> None:
    """Main function."""
    board = GameBoard()  # create the game board
    player_set = game_config()  # create players x and o
    move_counter = 0  # track how many moves have been played
    winner = None  # winning player

    print(board)

    # Main loop
    while (winner := board.check_winner()) is None:
        # Increase the number of moves made
        if (move_counter := move_counter + 1) == 10:
            print("\nGame over.  Draw.")
            exit(0)

        # Get a move
        if player_set.active.ai:
            print(f"\n{player_set.active}'s turn")
            move = board.generate_move()
            time.sleep(1)
        else:
            move = board.get_move(player_set.active)
            if not move:
                continue

        # Update the board
        board.mark(player_set.active, move)
        print(board)

        # Swap whose turn it is
        player_set.switch_player()

    print(f"\nGame over! {winner} wins.")


# __main__? Program entry point
if __name__ == "__main__":
    main()
