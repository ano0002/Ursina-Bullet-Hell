from ursina import *
from bullet import Bullet
from shader import bullet_shader

class ControllerPlayer(Entity):
    def __init__(self, bullets, team = 0, speed = 5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         color=color.azure,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team

    def update(self):
        lx,ly,rx,ry,lt,rt = held_keys['gamepad left stick x'], held_keys["gamepad left stick y"], held_keys["gamepad right stick x"], held_keys["gamepad right stick y"], held_keys["gamepad left trigger"], held_keys["gamepad right trigger"]
        self.velocity = Vec3(lx, ly, 0).normalized()*max(abs(lx), abs(ly))
        self.position += self.velocity * time.dt * self.SPEED
        if lx != 0 or ly != 0:
            self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

    def input(self, key):
        if key == "gamepad a":
            for bullet in self.bullets:
                if bullet.available:
                    bullet.team = self.team
                    bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                    bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z)), math.cos(math.radians(self.rotation_z))) * 0.2
                    break


class KeyboadPlayer(Entity):
    def __init__(self, bullets, team= 0, speed=5, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='cube',
                         texture="player",
                         color=color.green,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team

    def update(self):
        lx,ly = held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']
        self.velocity = Vec3(lx,ly, 0).normalized()
        self.position += self.velocity * time.dt * self.SPEED

        if lx != 0 or ly != 0:        
            self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

    def input(self, key):
        if key == "space":
            for bullet in self.bullets:
                if bullet.available:
                    bullet.team = self.team
                    bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                    bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z)), math.cos(math.radians(self.rotation_z))) * 0.2
                    break

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    camera.shader = bullet_shader
    bullets = [Bullet(Vec2(1,1), Vec2(0,0)) for _ in range(1000)]
    p1 = ControllerPlayer(bullets)
    p2 = KeyboadPlayer(bullets, team=1)

    def update():
        
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])
        
        for bullet in bullets:
            bullet.update()
            if bullet.get_world_position().x > 16*camera.aspect_ratio or bullet.get_world_position().x < -16*camera.aspect_ratio or bullet.get_world_position().y > 16 or bullet.get_world_position().y < -16:
                bullet.position = Vec2(1,1)

    
    app.run()