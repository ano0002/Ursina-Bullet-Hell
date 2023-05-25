from ursina import *
import time
from bullet import Bullet
from shader import bullet_shader

class Player(Entity):
    def __init__(self, bullets, team= 0, speed=5, lives = 3, add_to_scene_entities=True,left = False, controls = {"up":"w","down":"s","right":"d","left":"a","shoot":"space","dash":"left mouse down"}, **kwargs):
        super().__init__(add_to_scene_entities,
                         model='quad',
                         texture="player",
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team
        self.lives = lives
        self.last_dash = 0
        self.controls = controls
        if lives != float('inf'):
            if not left :
                self.heart_containers = [Entity(model="quad", parent = camera.ui, texture="heart", scale=0.03, color=color.red, position=Vec2(0.5*camera.aspect_ratio-i*0.035-0.0175,0.48)) for i in range(lives)]
            else:
                self.heart_containers = [Entity(model="quad", parent = camera.ui, texture="heart", scale=0.03, color=color.azure, position=Vec2(-0.5*camera.aspect_ratio+i*0.035+0.0175,0.48)) for i in range(lives)]

    def update(self):
        if self.lives > 0:
            lx,ly = held_keys[self.controls["right"]] - held_keys[self.controls["left"]], held_keys[self.controls["up"]] - held_keys[self.controls["down"]]
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
        if key == self.controls["shoot"]:
            self.shoot()
        if key == self.controls["dash"]:
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
    p1 = Player(bullets, controls={"up":"gamepad left stick y",
                                   "down":"",
                                   "right":"gamepad left stick x",
                                   "left":"",
                                   "shoot":"gamepad a",
                                   "dash":"gamepad start"},
                                   team=0, left = True)
    p2 = Player(bullets, team=1)

    def update():
        
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])
        
        for bullet in bullets:
            bullet.update()
            if bullet.get_world_position().x > 16*camera.aspect_ratio or bullet.get_world_position().x < -16*camera.aspect_ratio or bullet.get_world_position().y > 16 or bullet.get_world_position().y < -16:
                bullet.position = Vec2(1,1)

    
    app.run()