import tkinter as tk
from tkinter import font
from typing import List, Tuple, Optional

class Move:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

class TicTacToeGame:
    def __init__(self, board_size: int = 3):
        self.board_size = board_size
        self._setup_board()
        self._player = "X"
        self._has_winner = False
        self._move_count = 0

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self) -> List[List[Tuple[int, int]]]:
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def switch_player(self):
        self._player = "O" if self._player == "X" else "X"

    def check_winner(self, row: int, col: int) -> Optional[str]:
        for combo in self._winning_combos:
            if (row, col) in combo and all(
                self._current_moves[r][c].row == row and self._current_moves[r][c].col == col for r, c in combo):
                self._has_winner = True
                return self._player
        return None

    def reset_game(self):
        self._setup_board()
        self._player = "X"
        self._has_winner = False
        self._move_count = 0


class TicTacToeBoard(tk.Tk):
    def __init__(self, game: TicTacToeGame):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    command=lambda row=row, col=col: self._on_button_click(row, col)
                )
                self._cells[(row, col)] = button
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def _on_button_click(self, row: int, col: int):
        if self._game._has_winner or self._cells[(row, col)]["text"]:
            return

        current_player = self._game._player
        self._cells[(row, col)]["text"] = current_player
        self._cells[(row, col)]["fg"] = "blue" if current_player == "X" else "red"
        self._game._current_moves[row][col] = Move(row, col)
        self._game._move_count += 1

        winner = self._game.check_winner(row, col)
        if winner:
            self.display["text"] = f"Player {winner} wins!"
        elif self._game._move_count == 9:
            self.display["text"] = "It's a tie!"
        else:
            self._game.switch_player()
            self.display["text"] = f"Player {self._game._player}'s turn"

    def reset(self):
        self._game.reset_game()
        for button in self._cells.values():
            button["text"] = ""
            button["fg"] = "black"
        self.display["text"] = "Ready?"


def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
