from ursina import *
import csv


class Tileset():
    def __init__(self,tileset_file,tile_size=Vec2(16,16)) -> None:
        self.tileset = tileset_file
        self.tile_size = tile_size
        self.tileset_size = Vec2(load_texture(tileset_file).width//tile_size.x, load_texture(tileset_file).height//tile_size.y)
        self.tiles = self.generate_tiles(tileset_file)
        
    def generate_tiles(self,tileset_file):
        return []

class Tilemap(Entity):
    def __init__(self,map_file,tileset) -> None:
        self.tileset = tileset
        self.tiles = self.generate_map(map_file)
        
    def generate_map(self,map_file):
        
        width,height,layer = self.parse_csv(map_file)
        
        tiles = [[None for y in range(height)] for x in range(width)]
        tileset_size = self.tileset.tileset_size
        texture= self.tileset.tileset
        print(tileset_size)
        for y,lines in enumerate(layer):
            for x,gid in enumerate(lines):
                tile_coord = Vec2(gid%tileset_size.x,
                                  tileset_size.y-1-(gid//tileset_size.x))
                print(gid,tile_coord,tileset_size)
                tiles[x][y] = Entity(model='quad', texture=texture,
                                    tileset_size = tileset_size,tile_coordinate = tile_coord,
                                    position=(Vec3(x,y,1)-Vec3(width/2-.5,15.5,0))*Vec3(1,-1,1))
        return tiles
    
    def parse_csv(self,map_file):
        with open(map_file) as csv_file:
            layer = [[int(x) for x in row.split(",")] for row in csv_file]
        width,height = (len(layer[0]),len(layer))
        return width,height,layer
        
if __name__ == "__main__":
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    tileset = Tileset("./assets/tileset.png")
    tilemap = Tilemap("./assets/maps/map.csv",tileset)
    app.run()