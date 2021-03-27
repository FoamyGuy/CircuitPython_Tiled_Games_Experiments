import displayio
import board
import ugame

# Make the display context. Change size if you want
from TiledGameMap import TiledGameMap

display = board.DISPLAY

# Make the display context
main_group = displayio.Group(max_size=10)
display.show(main_group)

my_game = TiledGameMap("good_map_2.json")

main_group.append(my_game)

# Variable to old previous button state
prev_btn_vals = ugame.buttons.get_pressed()
_new_loc = {"x": my_game.player_loc["x"], "y": my_game.player_loc["y"]}
_moved = False
while True:
    cur_btn_vals = ugame.buttons.get_pressed()  # update button sate

    _new_loc = {"x": my_game.player_loc["x"], "y": my_game.player_loc["y"]}
    # if up button was pressed
    if not prev_btn_vals & ugame.K_UP and cur_btn_vals & ugame.K_UP:
        _new_loc["y"] = _new_loc["y"] - 1
        _moved = True
    # if down button was pressed
    if not prev_btn_vals & ugame.K_DOWN and cur_btn_vals & ugame.K_DOWN:
        _new_loc["y"] = _new_loc["y"] + 1
        _moved = True
    # if right button was pressed
    if not prev_btn_vals & ugame.K_RIGHT and cur_btn_vals & ugame.K_RIGHT:
        _new_loc["x"] = _new_loc["x"] + 1
        _moved = True
    # if left button was pressed
    if not prev_btn_vals & ugame.K_LEFT and cur_btn_vals & ugame.K_LEFT:
        _new_loc["x"] = _new_loc["x"] - 1
        _moved = True

    if _moved:
        print(_new_loc)
        print(my_game.player_loc)
        _moved = False
        print("loc changed")
        _tile_is_movable = my_game.is_tile_moveable(_new_loc)
        print("tile is moveable {}".format(_tile_is_movable))
        if _tile_is_movable:
            my_game.player_loc["x"] = _new_loc["x"]
            my_game.player_loc["y"] = _new_loc["y"]

        # update the the player sprite position
        my_game.update_player_location()

    # update the previous values
    prev_btn_vals = cur_btn_vals
