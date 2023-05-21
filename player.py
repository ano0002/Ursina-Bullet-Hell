from ursina import *
from controller import XboxController 


class ControllerPlayer(Entity):
    def __init__(self, speed = 5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         color=color.azure,
                         **kwargs)
        self.controller = XboxController()
        self.SPEED = speed
        
    def update(self):
        lx,ly,rx,ry,lt,rt = self.controller.read()
        self.velocity = Vec3(lx, ly, 0).normalized()*max(abs(lx), abs(ly))
        self.position += self.velocity * time.dt * self.SPEED
        if lx != 0 or ly != 0:        
            self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

    def input(self, key):
        if key == "gamepad a":
            print("A pressed")
            if self.color == color.azure:
                self.color = color.white
            else :
                self.color = color.azure


class KeyboadPlayer(Entity):
    def __init__(self, speed=5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         color=color.green,
                         **kwargs)
        self.SPEED = speed
        
    def update(self):
        lx,ly = held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']
        self.velocity = Vec3(lx,ly, 0).normalized()
        self.position += self.velocity * time.dt * self.SPEED
        
        if lx != 0 or ly != 0:        
            self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    p1 = ControllerPlayer()
    p2 = KeyboadPlayer()
    app.run()