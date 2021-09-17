# To open in Tiled
File -> open -> find and choose JSON file


# To create a map in Tiled
- File -> New
- Orientation: orthogonal, Tile layer format: CSV, Tile render order: right down
- set Map size height and width in tiles
- set tile size height and width 16px
- click Save as
- choose file name and location, filename should have .xml extension
- use file type default `Tiled map files`
- Make New Tileset
    - choose a name "default_tileset" or whatever you like
    - Type: based on tileset image
    - Yes embed in map
    - Click browse
    - find BMP tilesheet image
    - set tile height and width (16px)
    - set margin and spacing based on spritesheet (0px)
    - Check use transparent color
        - set custom color based on spritesheet bmp (#00FF00)
- Rename Tile Layer 1 to "background"
- make a new layer "entity"
- set properties on the tiles in the tileset
    - right click tileset name tab -> Edit Tileset
    - click tile
    - right click in Custom Properties -> add property
        - name property for `get_tile_name()`
        - can_walk property for player movement
        - player property for specifying the player entity
    - save tileset Ctrl-S
- add floors and walls to background layer
- add entities and player to entities layer
- save map Ctrl-S

- File -> Export As
    - set type JSON map files
    - choose name and location, name should include .json extension
    - copy .json file to `CIRCUITPY`


# Misc info
Tile indexes inside of Tiled json maps are 1 based.

0 index represents nothing in that tile


