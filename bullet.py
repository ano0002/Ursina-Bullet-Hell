from ursina import *
from shader import bullet_shader
import random

class Bullet():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
    
    def update(self):
        self.position += self.velocity * time.dt
    
    def get_world_position(self):
        return Vec2(self.position.x*32*camera.aspect_ratio,self.position.y*32)

    def get_position(self):
        return self.position



if __name__ == "__main__":
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    camera.shader = bullet_shader

    Entity(model='sphere', color=color.yellow, position=Vec2(16*camera.aspect_ratio,0))
    
    EditorCamera()
    bullets = [Bullet(Vec2(0,0), Vec2((random.random()*2-1)*0.01,(random.random()*2-1)*0.01)) for _ in range(1000)]

    def update():
        
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])
        
        for bullet in bullets:
            bullet.update()
            if bullet.get_world_position().x > 16*camera.aspect_ratio or bullet.get_world_position().x < -16*camera.aspect_ratio or bullet.get_world_position().y > 16 or bullet.get_world_position().y < -16:
                bullet.position = Vec2(0,0)

    app.run()