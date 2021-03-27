# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""

"""
import displayio
import json
import terminalio
from adafruit_display_text import label
from blinka_displayio_pygamedisplay import PyGameDisplay
import adafruit_imageload

f = open("midevil_map_1.json", "r")
map_obj = json.loads(f.read())
f.close()

# Make the display context. Change size if you want
display = PyGameDisplay(width=160 * 2, height=128 * 2)

# Make the display context
main_group = displayio.Group(max_size=10)
display.show(main_group)


# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("midevil_pink.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Load the sprite sheet (bitmap)
sprite_sheet2, palette2 = adafruit_imageload.load("midevil_pink.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)



palette.make_transparent(0)

# Create the sprite TileGrid
"""
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=16,
                            tile_height=16,
                            default_tile=0)

"""
# Create the castle TileGrid

castle = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=10,
                            height=8,
                            tile_width=16,
                            tile_height=16,
                            default_tile=0)

# Create the castle TileGrid
entities = displayio.TileGrid(sprite_sheet2, pixel_shader=palette2,
                              width=10,
                              height=8,
                              tile_width=16,
                              tile_height=16,
                              default_tile=88)

# Create a Group to hold the sprite and add it
entity_group = displayio.Group(scale=2)
entity_group.append(entities)

# Create a Group to hold the sprite and add it
#sprite_group = displayio.Group(scale=2)
#sprite_group.append(sprite)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=2)
castle_group.append(castle)

# Add the sprite and castle to the group

main_group.append(castle_group)
#main_group.append(entity_group)
#main_group.append(sprite_group)


for index, tile_index in enumerate(map_obj['layers'][0]['data']):
    _y = index // map_obj["width"]
    _x = index % map_obj["width"]
    print("{}, {} = {}".format(_x, _y, tile_index - 1))
    castle[_x, _y] = tile_index - 1

"""
print("=====")
for index, tile_index in enumerate(map_obj['layers'][1]['data']):
    _y = index // map_obj["width"]
    _x = index % map_obj["width"]


    if tile_index != 0:
        print("{}, {} = {}".format(_x, _y, tile_index - 1))
        entities[_x, _y] = tile_index - 1
    else:
        print("{}, {} = {}".format(_x, _y, 15))
        entities[_x, _y] = 15


    print(entities[_x, _y])
"""
"""
for y in range (8):
    for x in range(10):
        print(entities[x,y])
"""

#entities[3, 3] = 15
#entities[7, 3] = 15

#entities[3, 3] = 3
"""
# Castle tile assignments
# corners
castle[0, 0] = 6  # upper left
castle[9, 0] = 8  # upper right
castle[0, 7] = 12  # lower left
castle[9, 7] = 14  # lower right
# top / bottom walls
for x in range(1, 9):
    castle[x, 0] = 7  # top
    castle[x, 7] = 13  # bottom
# left/ right walls
for y in range(1, 7):
    castle[0, y] = 9  # left
    castle[9, y] = 11  # right
# floor
for x in range(1, 5):
    for y in range(1, 4):
        castle[x, y] = 10  # floor

"""
# put the sprite somewhere in the castle
#sprite.x = 2 * 16
#sprite.y = 3 * 16

while display.running:
    pass
