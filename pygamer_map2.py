# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""
import displayio
import board
import json
import terminalio
import ugame
from adafruit_display_text import label
import adafruit_imageload

"""
_tile_dict = {
    7: {
        "can_walk": False
    }
}
"""


def is_tile_moveable(tile_coords):
    """
    Check the can_walk property of the tile at the given coordinates
    :param tile_coords: dictionary with x and y entries
    :return: True if the player can walk on this tile. False otherwise.
    """

    _layer_can_walks = []

    _index = (tile_coords['y'] * map_obj["width"]) + tile_coords['x']
    print("index {}".format(_index))
    for layer in map_obj['layers']:
        tile_type = layer['data'][_index]
        tile_type = max(tile_type - 1, 0)

        if "can_walk" in tile_properties[tile_type]:
            # print("can_walk {}".format(tile_properties[tile_type]["can_walk"]))
            _layer_can_walks.append(tile_properties[tile_type]["can_walk"])
        else:
            _layer_can_walks.append(False)

    if False in _layer_can_walks:
        return False

    return True


player_loc = {"x": 4, "y": 3}

f = open("good_map_2.json", "r")
map_obj = json.loads(f.read())
f.close()

tile_properties = {0: {"can_walk": True}}

if "tiles" in map_obj['tilesets'][0]:
    print("has tiles")
    for _tile in map_obj['tilesets'][0]['tiles']:
        _tile_id = _tile["id"]
        if _tile_id not in tile_properties:
            tile_properties[_tile_id] = {}
        for _property in _tile["properties"]:
            tile_properties[_tile_id][_property["name"]] = _property["value"]

print(tile_properties)

# Make the display context. Change size if you want
display = board.DISPLAY

# Make the display context
main_group = displayio.Group(max_size=10)
display.show(main_group)

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("sprite_sheet_new.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

palette.make_transparent(0)
# Create the sprite TileGrid
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=16,
                            tile_height=16,
                            default_tile=0)

# Create the castle TileGrid
castle = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=10,
                            height=8,
                            tile_width=16,
                            tile_height=16,
                            default_tile=15)

# Create the castle TileGrid
entities = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                              width=10,
                              height=8,
                              tile_width=16,
                              tile_height=16,
                              default_tile=17)

# Create a Group to hold the sprite and add it
entity_group = displayio.Group(scale=1)
entity_group.append(entities)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group(scale=1)
sprite_group.append(sprite)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=1)
castle_group.append(castle)

# Add the sprite and castle to the group

main_group.append(castle_group)
main_group.append(entity_group)
main_group.append(sprite_group)

for index, tile_index in enumerate(map_obj['layers'][0]['data']):
    _y = index // map_obj["width"]
    _x = index % map_obj["width"]
    # print("{}, {} = {}".format(_x, _y, tile_index - 1))
    castle[_x, _y] = tile_index - 1

# print("=====")
for index, tile_index in enumerate(map_obj['layers'][1]['data']):
    _y = index // map_obj["width"]
    _x = index % map_obj["width"]

    if tile_index != 0:
        # print("{}, {} = {}".format(_x, _y, tile_index - 1))
        entities[_x, _y] = tile_index - 1
    else:
        # print("{}, {} = {}".format(_x, _y, 15))
        entities[_x, _y] = 15

    # print(entities[_x, _y])

"""
for y in range (8):
    for x in range(10):
        print(entities[x,y])
"""

entities[4, 3] = 15

# put the sprite somewhere in the castle
sprite.x = 16 * player_loc["x"]
sprite.y = 16 * player_loc["y"]

# Variable to old previous button state
prev_btn_vals = ugame.buttons.get_pressed()
_new_loc = {"x": player_loc["x"], "y": player_loc["y"]}
_moved = False
while True:
    cur_btn_vals = ugame.buttons.get_pressed()  # update button sate

    _new_loc = {"x": player_loc["x"], "y": player_loc["y"]}
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
        print(player_loc)
        _moved = False
        print("loc changed")
        _tile_is_movable = is_tile_moveable(_new_loc)
        print("tile is moveable {}".format(_tile_is_movable))
        if _tile_is_movable:
            player_loc = {"x": _new_loc["x"], "y": _new_loc["y"]}

    # update the the player sprite position
    sprite.x = 16 * player_loc["x"]
    sprite.y = 16 * player_loc["y"]

    # update the previous values
    prev_btn_vals = cur_btn_vals
