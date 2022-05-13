import sys
import random
import ctypes
from tkinter import Label, Button, PhotoImage
from utils import height_percentage, width_percentage
from settings import GRID_SIZE, MINES_COUNT, CELL_COUNT

width = int(width_percentage(70) / GRID_SIZE)
height = int(height_percentage(70) / GRID_SIZE)


class Cell:
    all = []
    cell_count = CELL_COUNT
    cell_count_label = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_open = False
        self.is_mine_candidate = False
        self.cell_btn = None

        Cell.all.append(self)

    @property
    def surrounding_cells(self):
        return [cell for cell in Cell.all if self._is_surrounding_cell(cell.x, cell.y)]

    @property
    def surrounding_mines(self):
        return [mine for mine in self.surrounding_cells if mine.is_mine]

    @property
    def surrounding_mines_count(self):
        return len(self.surrounding_mines)

    def create_btn(self, location):
        image = PhotoImage()
        btn = Button(
            location,
            bg='lightgray',
            image=image,
            width=width,
            height=height,
            compound='center'
        )

        btn.bind('<Button-1>', self._left_click_actions)  # Left click
        btn.bind('<Button-3>', self._right_click_actions)  # Right Click

        self.cell_btn = btn

    @staticmethod
    def create_cell_count_label(location):
        Cell.cell_count_label = Label(
            location,
            bg='black',
            fg='white',
            text=f'Cells Left: {Cell.cell_count}',
            font=('', 30)
        )

    def _left_click_actions(self, _):
        if not self.is_mine_candidate:
            if self.is_mine:
                self._show_mine()
            else:
                if self.surrounding_mines_count == 0:
                    for cell in self.surrounding_cells:
                        cell.show_cell()
                self.show_cell()
                if Cell.cell_count == MINES_COUNT:
                    ctypes.windll.user32.MessageBoxW(0, 'You win the game!', 'Congratulations', 0)

    def _right_click_actions(self, _):
        if not self.is_open:
            image = PhotoImage()
            self.cell_btn.configure(image=image, bg='lightgray' if self.is_mine_candidate else 'orange')
            self.is_mine_candidate = not self.is_mine_candidate

    def _show_mine(self):
        """Interrupts the game and displays a message that player lost!"""
        image = PhotoImage()
        self.cell_btn.configure(image=image, bg='red')

        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine!', 'Game Over', 0)
        sys.exit()

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            image = PhotoImage()
            self.cell_btn.configure(image=image, bg='white', text=f'{self.surrounding_mines_count}')
            # replace the text of the count with the new value
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(text=f'Cells Left: {Cell.cell_count}')

        # Mark the cell as opened we could unbind the event after opening the cell
        self.is_open = True

    def _is_surrounding_cell(self, x, y):
        """Check if the specified axis is surrounding the current cell"""
        if x == self.x and y == self.y:
            return False
        if x - 1 <= self.x <= x + 1 and y - 1 <= self.y <= y + 1:
            return True
        else:
            return False

    @staticmethod
    def randomize_mines():
        cells_to_mine = random.sample(Cell.all, MINES_COUNT)
        for cell in cells_to_mine:
            cell.is_mine = True

    def __repr__(self):
        return f'Cell({self.x}, {self.y}, {self.is_mine})'
