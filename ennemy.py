from ursina import *
from ursina.prefabs.health_bar import HealthBar

from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from player import ControllerPlayer, KeyboadPlayer
import math


class Ennemy(Entity):
    def func():
        pass
    def __init__(self, bullets,lives=1, team= 1, speed=5,texture = "turret", on_death=func, **kwargs):
        super().__init__(model='quad',
                         texture=texture,
                         color=color.red,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team
        self.total_alive = 0
        self.lives = lives
        self.ondeath = on_death
        self.bullets_shot = []
        
    def update(self):
        if self.lives > 0:
            
            self.total_alive += time.dt
            
            if self.shot():
                self.lives -= 1
            
            if hasattr(self,"custom_update"):
                self.custom_update()

            for bullet in self.bullets_shot:
                if bullet.available:
                    self.bullets_shot.remove(bullet)
            
        else:
            self.die()
            destroy(self)

    def shoot(self,angle=0, speed=1):
        for bullet in self.bullets:
            if bullet.available:
                bullet.team = self.team
                bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z+angle)), math.cos(math.radians(self.rotation_z+angle))) * 0.2 * speed
                self.bullets_shot.append(bullet)
                break
    
    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.4:
                        bullet.available = True
                        return True
        return False

    def die(self):
        self.ondeath()
        pass

class SpiralEnnemy(Ennemy):
    def __init__(self, bullets,speed = 5,fire_rate= 5, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)

    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            self.shoot()
            self.total_alive = 0
        self.rotation_z += self.SPEED*5*time.dt

class DoubleSpiralEnnemy(Ennemy):
    def __init__(self, bullets,speed = 5,fire_rate= 5, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate,texture="2xturret", **kwargs)

    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            self.shoot()
            self.shoot(180)
            self.total_alive = 0
        self.rotation_z += self.SPEED*5*time.dt

class QuadrupleSpiralEnnemy(Ennemy):
    def __init__(self, bullets,speed = 5,fire_rate= 5, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate,texture="4xturret", **kwargs)
    
    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            self.shoot()
            self.shoot(180)
            self.shoot(90)
            self.shoot(-90)
            self.total_alive = 0
        self.rotation_z += self.SPEED*5*time.dt

class MachineGunEnnemy(Ennemy):
    def __init__(self, bullets,speed = 5,fire_rate= 25, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
    
    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            self.shoot(random.random() * 360,0.2)
            self.total_alive = 0
        
        for bullet in self.bullets_shot:
            if distance_2d(bullet.get_world_position(),self.position) > 4:
                bullet.available = True
        
class AimerEnnemy(Ennemy):
    def __init__(self, bullets,targets,speed = 5,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
        self.targets = targets
        self.last_bullet = 0
    
    def custom_update(self):
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position - Vec3(0.8,0.8,0))
        if self.total_alive > 1/self.fire_rate:
            if self.total_alive-self.last_bullet > 0.03:
                self.shoot()
                self.last_bullet = self.total_alive
            if self.total_alive > 1/self.fire_rate+0.1:
                self.total_alive = 0
                self.last_bullet = 0

class PatrolEnnemy(Ennemy):
    def __init__(self, bullets, waypoints, targets,speed =0.2,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.targets = targets
        self.last_bullet = 0
        self.position = self.waypoints[self.current_waypoint]
    
    def custom_update(self):
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position - Vec3(0.8,0.8,0))
            
        if self.total_alive > 1/self.fire_rate:
            if self.total_alive-self.last_bullet > 0.03:
                self.shoot()
                self.last_bullet = self.total_alive
            if self.total_alive > 1/self.fire_rate+0.1:
                self.total_alive = 0
                self.last_bullet = 0

        
        if distance_2d(self.position,self.waypoints[self.current_waypoint]) < 0.1:
            self.current_waypoint = (self.current_waypoint+1)%len(self.waypoints)
            self.animate_position(self.waypoints[self.current_waypoint],duration=1/self.SPEED,curve=curve.linear)

class LaserEnnemy(Ennemy):
    def __init__(self, bullets,speed = 5,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
        self.last_bullet = 0
    
    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            if self.total_alive-self.last_bullet > 0.01:
                self.shoot(speed=5)
                self.last_bullet = self.total_alive
            if self.total_alive > 1/self.fire_rate+0.6:
                self.total_alive = 0
                self.last_bullet = 0
        self.rotation_z += self.SPEED*5*time.dt

class Boss(Ennemy):
    def __init__(self, bullets, waypoints, targets,speed =0.2,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,scale =2,fire_rate = fire_rate, **kwargs)
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.targets = targets
        self.last_bullet = 0
        self.position = self.waypoints[self.current_waypoint]
        self.life_bar = HealthBar(max_value=self.lives,roundness=0,show_text=False,bar_color=color.red,animation_duration=0,position = Vec2(-0.25,-0.45),parent = camera.ui)
    
    def custom_update(self):
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position - Vec3(0.4))
            
        if self.total_alive > 1/self.fire_rate:
            if self.total_alive-self.last_bullet > 0.03:
                self.shoot()
                self.last_bullet = self.total_alive
            if self.total_alive > 1/self.fire_rate+0.1:
                self.total_alive = 0
                self.last_bullet = 0

        self.life_bar.value = self.lives
        
        if distance_2d(self.position,self.waypoints[self.current_waypoint]) < 0.1:
            self.current_waypoint = (self.current_waypoint+1)%len(self.waypoints)
            self.animate_position(self.waypoints[self.current_waypoint],duration=1/self.SPEED,curve=curve.linear)

    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.8:
                        bullet.available = True
                        return True
        return False

    def die(self):
        self.life_bar.enabled = False
        super().die()


if __name__ == "__main__":

    app = Ursina(development_mode=True)

    camera.orthographic = True
    camera.fov = 32


    tileset = Tileset("./assets/tileset.png")
    tilemap = Tilemap("./assets/maps/map.csv",tileset)

    camera.shader = bullet_shader
    bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

    p1 = KeyboadPlayer(bullets,team=0, lives=float('inf'))
    #p2 = ControllerPlayer(bullets, team=0, lives=float('inf'))
    
    players = [p1]
    
    MachineGunEnnemy(bullets, position=Vec2(-5,5))
    SpiralEnnemy(bullets, position=Vec2(0,5))
    DoubleSpiralEnnemy(bullets, position=Vec2(5,5))    
    QuadrupleSpiralEnnemy(bullets, position=Vec2(10,5))
    AimerEnnemy(bullets, players, position=Vec2(-10,5))
    PatrolEnnemy(bullets, [Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)],players, position=Vec2(0,0))
    Boss(bullets, [Vec2(-10,-5),Vec2(10,-5)],players, position=Vec2(0,-5), lives=50)
    LaserEnnemy(bullets, position=Vec2(0,10))


    def update():
        for bullet in bullets:
            bullet.update()
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])


    app.run()
