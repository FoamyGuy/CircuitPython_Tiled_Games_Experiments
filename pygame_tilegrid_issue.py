# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import adafruit_imageload

# Make the display context. Change size if you want
display = PyGameDisplay(width=160 * 2, height=128 * 2)

# Make the display context
main_group = displayio.Group(max_size=10)
display.show(main_group)

sprite_sheet, palette = adafruit_imageload.load("sprite_sheet_diff.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create the castle TileGrid
entities = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                              width=10,
                              height=8,
                              tile_width=16,
                              tile_height=16,
                              default_tile=17)

# Create a Group to hold the sprite and add it
entity_group = displayio.Group(scale=2)
entity_group.append(entities)

main_group.append(entity_group)

palette.make_transparent(20)
entities[3, 3] = 0

while display.running:
    pass
