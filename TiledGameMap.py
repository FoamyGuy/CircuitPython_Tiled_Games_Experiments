from displayio import Group, TileGrid, Bitmap, Palette
import json
import adafruit_imageload


class TiledGameMap(Group):

    def __init__(self, map_json_file):
        super().__init__()
        f = open("good_map_2.json", "r")
        self._map_obj = json.loads(f.read())
        f.close()

        self.player_loc = {"x": 1, "y": 1}

        self._tile_properties = {0: {"can_walk": True}}

        if "tiles" in self.map_obj['tilesets'][0]:
            print("has tiles")
            for _tile in self.map_obj['tilesets'][0]['tiles']:
                _tile_id = _tile["id"]
                if _tile_id not in self.tile_properties:
                    self.tile_properties[_tile_id] = {}
                for _property in _tile["properties"]:
                    self.tile_properties[_tile_id][_property["name"]] = _property["value"]

        _sprite_sheet_image = self.map_obj["tilesets"][0]["image"]
        # Load the sprite sheet (bitmap)
        self._sprite_sheet, self._palette = adafruit_imageload.load(_sprite_sheet_image,
                                                                    bitmap=Bitmap,
                                                                    palette=Palette)

        self._palette.make_transparent(0)
        # Create the background TileGrid
        self._background_tilegrid = TileGrid(self._sprite_sheet, pixel_shader=self._palette,
                                             width=10,
                                             height=8,
                                             tile_width=16,
                                             tile_height=16,
                                             default_tile=15)

        # Create the castle TileGrid
        self._entity_tilegrid = TileGrid(self._sprite_sheet, pixel_shader=self._palette,
                                         width=10,
                                         height=8,
                                         tile_width=16,
                                         tile_height=16,
                                         default_tile=17)

        # Create the sprite TileGrid
        self._sprite_tilegrid = TileGrid(self._sprite_sheet, pixel_shader=self._palette,
                                         width=1,
                                         height=1,
                                         tile_width=16,
                                         tile_height=16,
                                         default_tile=0)

        self.append(self._background_tilegrid)
        self.append(self._entity_tilegrid)
        self.append(self._sprite_tilegrid)

        self._load_tilegrids()

        # put the sprite somewhere in the castle
        self._sprite_tilegrid.x = 16 * self.player_loc["x"]
        self._sprite_tilegrid.y = 16 * self.player_loc["y"]


    def _load_tilegrids(self, x=1, y=2, width=10, height=8):

        def _build_tiles_list(layer_index):
            _tiles_to_load = []
            for _y in range(height):
                for _x in range(width):
                    _extra_offset = (self.map_obj["width"] - width) * _y
                    _tiles_to_load.append(
                        self.map_obj['layers'][layer_index]['data'][_x + _y * width + start_index + _extra_offset])
            return _tiles_to_load

        _extra_offset = (self.map_obj["width"] - width) * y
        start_index = y * width + x + _extra_offset
        print("start index {}".format(start_index))


        #_tiles_to_load = self.map_obj['layers'][0]['data'][start_index:start_index+count]

        _background_tiles = _build_tiles_list(0)
        for index, tile_index in enumerate(_background_tiles):
            _y = index // width
            _x = index % width
            # print("{}, {} = {}".format(_x, _y, tile_index - 1))
            self._background_tilegrid[_x, _y] = tile_index - 1

        _entity_tiles = _build_tiles_list(1)
        for index, tile_index in enumerate(_entity_tiles):
            _y = index // width
            _x = index % width

            if tile_index != 0:
                # print("{}, {} = {}".format(_x, _y, tile_index - 1))
                if self.get_tile_property(tile_index - 1, "player"):
                    # place player
                    self.player_loc["x"] = _x
                    self.player_loc["y"] = _y
                else:
                    # place non-player entity
                    self._entity_tilegrid[_x, _y] = tile_index - 1
            else:
                # put empty space for tile id 0
                # print("{}, {} = {}".format(_x, _y, 15))
                self._entity_tilegrid[_x, _y] = 15
    @property
    def map_obj(self):
        return self._map_obj

    @property
    def tile_properties(self):
        return self._tile_properties

    def get_tile_property(self, tile_id, property_name):
        if property_name in self.tile_properties[tile_id]:
            return self.tile_properties[tile_id][property_name]
        return None

    def update_player_location(self):
        self._sprite_tilegrid.x = 16 * self.player_loc["x"]
        self._sprite_tilegrid.y = 16 * self.player_loc["y"]

    def is_tile_moveable(self, tile_coords):
        """
        Check the can_walk property of the tile at the given coordinates
        :param tile_coords: dictionary with x and y entries
        :return: True if the player can walk on this tile. False otherwise.
        """

        _layer_can_walks = []

        _index = (tile_coords['y'] * self.map_obj["width"]) + tile_coords['x']
        print("index {}".format(_index))
        for layer in self.map_obj['layers']:
            tile_type = layer['data'][_index]
            tile_type = max(tile_type - 1, 0)

            if "can_walk" in self.tile_properties[tile_type]:
                # print("can_walk {}".format(tile_properties[tile_type]["can_walk"]))
                _layer_can_walks.append(self.tile_properties[tile_type]["can_walk"])
            else:
                _layer_can_walks.append(False)

        if False in _layer_can_walks:
            return False

        return True
