from settings import WIDTH, HEIGHT, GRID_SIZE
from cell import Cell
from utils import height_percentage, width_percentage
from tkinter import *

root = Tk()

# Override the settings of the window
root.configure(bg='black')
root.geometry(f'{WIDTH}x{HEIGHT}')
root.title('Minesweeper Game')
root.resizable(False, False)

top_frame_height = height_percentage(25)
top_frame = Frame(
    root,
    bg='black',
    width=WIDTH,
    height=top_frame_height
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper Game',
    font=('', 48)
)
game_title.place(x=width_percentage(25))

left_frame_width = width_percentage(25)
left_frame = Frame(
    root,
    bg='black',
    width=left_frame_width,
    height=HEIGHT - top_frame_height
)
left_frame.place(x=0, y=top_frame_height)

main_frame_width = width_percentage(75)
main_frame_height = height_percentage(75)
main_frame = Frame(
    root,
    width=main_frame_width,
    height=main_frame_height
)
main_frame.place(x=left_frame_width, y=top_frame_height)

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        c = Cell(x, y)
        c.create_btn(main_frame)
        c.cell_btn.grid(row=x, column=y)

# Call the label from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label.place(x=0, y=0)

Cell.randomize_mines()

# Run the window
root.mainloop()
