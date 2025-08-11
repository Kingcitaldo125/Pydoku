# Pydoku
Python/PyGame Sudoku

## Installing
Install pygame using `pip`:
```
pip install -r requirements.txt
```

## Playing

Start the game by running Python against the main file:
```
python main.py
```

After the game starts, you will be asked to enter in a difficulty setting.
Enter in your chosen difficulty setting in the terminal window you used to start the game.

To play, use the left and right mouse buttons to interact with the cells.
The left mouse button will **increment** a cell's value, up to and including `9`.
The right mouse button will **decrement** a cell's value, down to and including `1`.

If a cell's value is `1`, and a right-click were selected on it, this will clear the cell.

The game will actively track the win condition for you.
If the board is both completed and valid, the game will give you a visual indicator letting you know you've won.

Press the `Esc` key to quit out of the game at any time.
Progress is **not** saved.

## License
Pydoku is licensed under the Apache-2.0 license.
See the [license file](https://github.com/Kingcitaldo125/Pydoku/blob/main/LICENSE) for more details.
