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


import random

from typing import Callable, Tuple, Union


class Players:
    def __init__(self) -> None:
        """Create two players, player One is x, player Two is o.
        Player One starts the game.
        """
        self.players = {'One': 'x', 'Two': 'o'}
        self.player = self.players['One']
        self.computer = False

    def switch_player(self) -> None:
        """Switch active player."""
        if self.player == self.players['One']:
            self.player = self.players['Two']
        else:
            self.player = self.players['One']


class GameBoard():
    def __init__(self) -> None:
        """Create the game board, represented as a 3x3 matrix."""
        self.board = [['1', '2', '3'],
                      ['4', '5', '6'],
                      ['7', '8', '9']]
        self.moves = [n for n in range(1, 10)]

    def draw(self) -> None:
        """Draw the game board."""
        print()
        for row in self.board:
            print(row)

    def mark(self, player: str, square: Union[bool, int]) -> None:
        """Mark a square on the board as played.
        :param player: current player
        :param square: valid matrix index
        """
        row, col = square
        self.board[row][col] = player

    def validate_move(self, square: int) -> Union[bool, Tuple[int, int]]:
        """Check that a square is a valid play.
        :param square: int representing index of board matrix
        :return: valid row,col tuple or boolean False
        """
        # Square number should be from 1 to 9
        if square not in range(1, 10):
            print('Invalid square, enter 1-9')
            return False

        # Convert square number to a valid index on game board
        if square in range(1, 4):
            index = (0, square - 1)  # row one
        elif square in range(4, 7):
            index = (1, square - 4)  # row two
        else:
            index = (2, square - 7)  # row three

        # Check if square has already been played
        if square not in self.moves:
            print('\nSquare already taken')
            return False

        # remove square from available moves
        self.moves.remove(square)

        # Return index of square to mark
        row, col = index
        index = (row, col)
        return index

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

    def get_move(self, player: str) -> Union[bool, int]:
        """Get a move from a player.
        :param player: player whose turn it is
        :return: False or number representing a game board square
        """
        number = input(f"\n{player}'s turn, Enter a number: ")
        try:
            square = self.validate_move(int(number))
        except ValueError:
            print('Invalid input, try again.')
            return False

        return square

    def generate_move(self) -> int:
        """Generate a move for computer's turn.
        :return: Number representing a game board square
        """
        random_square = random.choice(self.moves)
        square = self.validate_move(random_square)

        return square


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
            print('\nProcess terminated.')
            exit(0)

    return wrapper


def game_config() -> bool:
    """Player must choose between Human vs Human or Human vs Computer.
    :return: Boolean value, True if human vs computer
    """
    while True:
        print('1) Human vs Human')
        print('2) Human vs Computer')

        game_type = input('\nGame type [1-2]: ')
        try:
            game_type = int(game_type)
        except ValueError:
            print('\nPlease enter 1 or 2\n')
            continue

        if game_type == 1:
            return False
        elif game_type == 2:
            return True
        else:
            print('\nPlease enter 1 or 2\n')

@catch_keyboard_interrupt
def main() -> None:
    """Main function."""
    players = Players()  # create players x and o
    board = GameBoard()  # create the game board
    move_counter = 0     # track how many moves have been played

    print('Tic-Tac-Toe\n')

    # Game type, if True, o is computer generated
    players.computer = game_config()

    # Draw the board
    board.draw()

    # Main loop
    while True:
        # Get a move
        if players.player == players.players['Two'] and players.computer:
            square = board.generate_move()
            print("\nComputer's turn")
        else:
            square = board.get_move(players.player)
        if not square:
            continue

        # Update the board
        board.mark(players.player, square)
        board.draw()

        # Swap whose turn it is
        players.switch_player()

        # Increase the number of moves made
        move_counter += 1
        if move_counter == 8:
            print('\nGame over.  Draw.')
            break

        # Check for a winner
        winner = board.check_winner()
        if winner is not None:
            print(f'\nGame over! {winner} wins.')
            break


# __main__? Program entry point
if __name__ == '__main__':
    main()
