

import displayio
import pygame

from blinka_displayio_pygamedisplay import PyGameDisplay

# Make the display context. Change size if you want
from TiledGameMap import TiledGameMap


display = PyGameDisplay(width=160 * 4, height=128 * 4)

# Make the display context
main_group = displayio.Group(max_size=10, scale=4)
display.show(main_group)

my_game = TiledGameMap("new_map_0.json")

main_group.append(my_game)

# Variable to old previous button state
#prev_btn_vals = ugame.buttons.get_pressed()

_new_loc = {"x": my_game.player_loc["x"], "y": my_game.player_loc["y"]}
_moved = False

print("initial player loc: {}".format(my_game.player_loc))
# print(my_game.tile_properties)

my_game.set_camera_loc({"x": 1, "y": 1})
while display.running:

    #cur_btn_vals = ugame.buttons.get_pressed()  # update button sate

    # _new_loc = {"x": my_game.player_loc["x"], "y": my_game.player_loc["y"]}
    _new_loc = {"x": my_game.cursor_loc["x"], "y": my_game.cursor_loc["y"]}

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("left")
                _new_loc["x"] = _new_loc["x"] - 1
                _moved = True
            if event.key == pygame.K_RIGHT:
                print("right")
                _new_loc["x"] = _new_loc["x"] + 1
                _moved = True
            if event.key == pygame.K_UP:
                print("up")
                _new_loc["y"] = _new_loc["y"] - 1
                _moved = True
            if event.key == pygame.K_DOWN:
                print("down")
                _new_loc["y"] = _new_loc["y"] + 1
                _moved = True
    """
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
    """

    if _moved:
        # print(_new_loc)
        # print(my_game.player_loc)
        _moved = False
        print("loc changed")
        """
        _tile_is_movable = my_game.is_tile_moveable(_new_loc)
        print("tile is moveable {}".format(_tile_is_movable))
        if _tile_is_movable:
            my_game.player_loc["x"] = _new_loc["x"]
            my_game.player_loc["y"] = _new_loc["y"]
            # update the the player sprite position
            my_game.update_player_location()
        """
        print(_new_loc)

        if my_game.map_obj["width"] > _new_loc["x"] >= 0 and my_game.map_obj["height"] > _new_loc["y"] >= 0:
            if _new_loc["x"] >= 10 + my_game.camera_loc["x"]:
                my_game.set_camera_loc({"x": my_game.camera_loc["x"] + 1, "y": my_game.camera_loc["y"]})
            if _new_loc["x"] < my_game.camera_loc["x"]:
                my_game.set_camera_loc({"x": my_game.camera_loc["x"] - 1, "y": my_game.camera_loc["y"]})

            if _new_loc["y"] >= 8 + my_game.camera_loc["y"]:
                my_game.set_camera_loc({"x": my_game.camera_loc["x"], "y": my_game.camera_loc["y"] + 1})
            if _new_loc["y"] < my_game.camera_loc["y"]:
                my_game.set_camera_loc({"x": my_game.camera_loc["x"], "y": my_game.camera_loc["y"] - 1})

            my_game.update_cursor_location(_new_loc)

    # if A button was pressed
    """
    if not prev_btn_vals & ugame.K_O and cur_btn_vals & ugame.K_O:
        print(my_game.get_tile_name(my_game.cursor_loc))

    # update the previous values
    prev_btn_vals = cur_btn_vals
    """
    #pygame.time.delay(10)
