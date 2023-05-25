from ursina import *
import time
from bullet import Bullet
from shader import bullet_shader

class ControllerPlayer(Entity):
    def __init__(self, bullets, team = 0, speed = 5, lives= 3, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='quad',
                         texture="player",
                         color=color.azure,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team
        self.lives = lives
        self.last_dash = 0
        if self.lives != float('inf'):
            self.heart_containers = [Entity(model="quad", parent = camera.ui, texture="heart", scale=0.03, color=color.azure, position=Vec2(-0.5*camera.aspect_ratio+i*0.035+0.0175,0.48)) for i in range(lives)]

    def update(self):
        if self.lives > 0:
            lx,ly,rx,ry,lt,rt = held_keys['gamepad left stick x'], held_keys["gamepad left stick y"], held_keys["gamepad right stick x"], held_keys["gamepad right stick y"], held_keys["gamepad left trigger"], held_keys["gamepad right trigger"]
            self.velocity = Vec3(lx, ly, 0).normalized()*max(abs(lx), abs(ly))
            self.position += self.velocity * time.dt * self.SPEED
            if lx != 0 or ly != 0:
                self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

            if self.shot():
                self.lives -= 1
                if self.lives != float('inf'):
                    self.heart_containers[self.lives].color = color.black
            
            if self.position.x > 16*camera.aspect_ratio:
                self.position.x = 16*camera.aspect_ratio
            if self.position.x < -16*camera.aspect_ratio:
                self.position.x = -16*camera.aspect_ratio
            
            if self.position.y > 16:
                self.position.y = 16
            if self.position.y < -16:
                self.position.y = -16
            
        else:
            self.die()
            destroy(self)
            for heart in self.heart_containers:
                destroy(heart)
    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.4:
                        bullet.available = True
                        return True
        return False

    def die(self):
        print("dead")
        pass

    def input(self, key):
        if key == "gamepad a":
            self.shoot()
        if key == "gamepad start":
            if self.last_dash+10 < time.time():
                self.dash()
                self.last_dash = time.time()
                
    def shoot(self):
        for bullet in self.bullets:
            if bullet.available:
                bullet.team = self.team
                bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z)), math.cos(math.radians(self.rotation_z))) * 0.2
                break

    @property
    def alive(self):
        return self.lives > 0

    def dash(self,dash_length = 3):
        self.animate_position(self.position + self.up* dash_length, duration=0.1, curve = curve.in_out_cubic)


class KeyboadPlayer(Entity):
    def __init__(self, bullets, team= 0, speed=5, lives = 3, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='quad',
                         texture="player",
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team
        self.lives = lives
        self.last_dash = 0
        if lives != float('inf'):
            self.heart_containers = [Entity(model="quad", parent = camera.ui, texture="heart", scale=0.03, color=color.red, position=Vec2(0.5*camera.aspect_ratio-i*0.035-0.0175,0.48)) for i in range(lives)]
        
    def update(self):
        if self.lives > 0:
            lx,ly = held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']
            self.velocity = Vec3(lx, ly, 0).normalized()*max(abs(lx), abs(ly))
            self.position += self.velocity * time.dt * self.SPEED
            if lx != 0 or ly != 0:
                self.rotation_z = -math.degrees(math.atan2(ly, lx))+90

            if self.shot():
                self.lives -= 1
                if self.lives != float('inf'):
                    self.heart_containers[self.lives].color = color.black
        else:
            self.die()
            destroy(self)
            for heart in self.heart_containers:
                destroy(heart)
            
    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.4:
                        bullet.available = True
                        return True
        return False

    def die(self):
        print("dead")
        pass

    def input(self, key):
        if key == "space":
            self.shoot()
        if key == "left mouse down":
            if self.last_dash+10 < time.time():
                self.dash()
                self.last_dash = time.time()

    def shoot(self):
        for bullet in self.bullets:
            if bullet.available:
                bullet.team = self.team
                bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z)), math.cos(math.radians(self.rotation_z))) * 0.2
                break

    @property
    def alive(self):
        return self.lives > 0

    def dash(self,dash_length = 3):
        self.animate_position(self.position + self.up* dash_length, duration=0.1, curve = curve.in_out_cubic)

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