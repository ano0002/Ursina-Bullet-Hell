from ursina import *


class Ennemy(Entity):
    def __init__(self, bullets, team= 1, speed=5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         color=color.red,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team


if __name__ == "__main__":
    app = Ursina()
    
    
    camera.orthographic = True
    camera.fov = 32
    
    
    
    app.run()
