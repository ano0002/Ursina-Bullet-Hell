from ursina import *
from controller import XboxController 


class ControllerPlayer(Entity):
    def __init__(self, speed = 5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         **kwargs)
        self.controller = XboxController()
        self.SPEED = speed
        
    def update(self):
        lx,ly,rx,ry,lt,rt = self.controller.read()
        self.velocity = Vec3(lx, ly, 0).normalized()*max(abs(lx), abs(ly))
        self.position += self.velocity * time.dt * self.SPEED
        self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

    def input(self, key):
        if key == "gamepad a":
            print("A pressed")
            if self.color == color.lightblue:
                self.color = color.white
            else :
                self.color = color.lightblue

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    p1 = ControllerPlayer()
    app.run()