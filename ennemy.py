from ursina import *
from ursina.prefabs.health_bar import HealthBar

from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from player import Player
import math

class Wave():
    def __init__(self,ennemies,delay,args={},next_wave = None) -> None:
        self.to_spawn = ennemies
        self.spawned = []
        self.spawned_total = 0
        self.spawned_alive = 0
        self.delay = delay
        self.next_wave = next_wave
        self.world = None
        self.args = args
        self.total_time = float("-inf")
    
    def start(self):
        self.total_time = 0
        if self.to_spawn == []:
            return
        for ennemy_type, args in self.to_spawn:
            self.spawned.append(ennemy_type(wave = self,world = self.world,**self.args,**args))
            self.spawned_total += 1
            self.spawned_alive += 1
        self.to_spawn = []
            

    def update(self):
        self.total_time += time.dt
        if self.total_time > self.delay:
            self.end()


    def end(self):
        if self.spawned_alive == 0:
            for player in self.world.players:
                if player.lives < 3 and player.lives > 0:
                    player.lives += 1
        if self.next_wave:
            self.next_wave.start()

class Ennemy(Entity):
    def func():
        pass
    def __init__(self, bullets,lives=1, team= 1, speed=5,texture = "turret", on_death=func, wave=None,total_alive = 0,world= None, **kwargs):
        super().__init__(model='quad',
                         texture=texture,
                         color=color.red,
                         **kwargs)
        self.SPEED = speed
        self.bullets = bullets
        self.team = team
        self.total_alive = total_alive
        self.lives = lives
        self.ondeath = on_death
        self.bullets_shot = []
        self.wave = wave
        self.world = world
        
    def update(self):
        if self.world != None:
            if not self.world.status == "paused":
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
                        self.ondeath()
                        if self.wave != None:
                            self.wave.spawned_alive -= 1
                            if self.wave.spawned_alive == 0:
                                self.wave.end()
                        self.die()
                        destroy(self)
                

    def shoot(self,angle=0, speed=1):
        try :
            for bullet in self.bullets:
                if bullet.available:
                    bullet.team = self.team
                    bullet.position = Vec2(self.position.x/(32*camera.aspect_ratio), self.position.y /32)
                    bullet.velocity = Vec2(math.sin(math.radians(self.rotation_z+angle))/camera.aspect_ratio, math.cos(math.radians(self.rotation_z+angle))) * 0.2 * speed
                    self.bullets_shot.append(bullet)
                    break
        except:
            pass
    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.4:
                        bullet.available = True
                        return True
        return False

    def die(self):
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
    def __init__(self, bullets,speed = 5,fire_rate= 2, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
    
    def custom_update(self):
        if self.total_alive > 1/self.fire_rate:
            for i in range(36):
                self.shoot(i*10,0.5)
            self.total_alive = 0
        
        for bullet in self.bullets_shot:
            if distance_2d(bullet.get_world_position(),self.position) > 4:
                bullet.available = True

    def die(self):
        for bullet in self.bullets_shot:
            bullet.available = True

class AimerEnnemy(Ennemy):
    def __init__(self, bullets,targets,speed = 5,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,fire_rate = fire_rate, **kwargs)
        self.targets = targets
        self.last_bullet = 0
    
    def custom_update(self):
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position)
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
        self.start_move = 0
        self.shooting_timer = 0
    
    def custom_update(self):
        self.shooting_timer += time.dt
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position)
            
        if self.shooting_timer > 1/self.fire_rate:
            if self.shooting_timer-self.last_bullet > 0.03:
                self.shoot()
                self.last_bullet = self.shooting_timer
            if self.shooting_timer > 1/self.fire_rate+0.1:
                self.shooting_timer = 0
                self.last_bullet = 0

        
        if distance_2d(self.position,self.waypoints[self.current_waypoint]) < 0.1:
            self.start_move = self.total_alive
            self.current_waypoint = (self.current_waypoint+1)%len(self.waypoints)
        else :
            self.position = lerp(self.waypoints[self.current_waypoint-1],self.waypoints[self.current_waypoint],(self.total_alive-self.start_move)/(1/self.SPEED))
            
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


class Boss1(Ennemy):
    def __init__(self, bullets, waypoints, targets,speed =0.2,fire_rate= 1, **kwargs):
        super().__init__(bullets, speed = speed,scale =2,fire_rate = fire_rate, **kwargs)
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.targets = targets
        self.last_bullet = 0
        self.position = self.waypoints[self.current_waypoint]
        self.life_bar = HealthBar(max_value=self.lives,roundness=0,show_text=False,bar_color=color.red,animation_duration=0,position = Vec2(-0.25,-0.45),parent = camera.ui)
        self.shooting_timer = 0
        self.shooting_8_corners_timer = 0
        self.angle = 0
    
    def custom_update(self):
        self.shooting_timer += time.dt
        self.shooting_8_corners_timer += time.dt
        if any(target.alive for target in self.targets):
            target = min(self.targets, key=lambda target: distance_2d(target.position,self.position) if target.alive else float('inf'))
            self.look_at_2d(target.position)
            
        if self.shooting_timer > 1/self.fire_rate:
            if self.shooting_timer-self.last_bullet > 0.03:
                self.shoot()
                self.shoot(-5)
                self.shoot(5)
                self.last_bullet = self.shooting_timer
            if self.shooting_timer > 1/self.fire_rate+0.1:
                self.shooting_timer = 0
                self.last_bullet = 0
        if self.shooting_8_corners_timer > 1/self.fire_rate:
            self.angle = self.shoot_8_corners(self.angle)
            self.shooting_8_corners_timer = 0
            
        self.life_bar.value = self.lives
        
        if distance_2d(self.position,self.waypoints[self.current_waypoint]) < 0.1:
            self.start_move = self.total_alive
            self.current_waypoint = (self.current_waypoint+1)%len(self.waypoints)
        else :
            self.position = lerp(self.waypoints[self.current_waypoint-1],self.waypoints[self.current_waypoint],(self.total_alive-self.start_move)/(1/self.SPEED))

    
    def shot(self):
        for bullet in self.bullets:
            if not bullet.available:
                if bullet.team != self.team:
                    if distance_2d(bullet.get_world_position(),self.position) < 0.8:
                        bullet.available = True
                        return True
                    
    
        return False

    def shoot_8_corners(self,angle=0):
        for i in range(8):
            self.shoot(45*i+angle)
        return angle+5

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

    p1 = Player(bullets, controls={"up":"gamepad left stick y",
                                    "down":"",
                                    "right":"gamepad left stick x",
                                    "left":"",
                                    "shoot":"gamepad a",
                                    "dash":"gamepad start"},
                                    left = True,
                                    lives=float('inf'))
    p2 = Player(bullets,lives=float('inf'))
    players = [p1,p2]
    
    wave = Wave(
        [
            (MachineGunEnnemy,{'position':Vec2(-5,5)}),
            (SpiralEnnemy,{'position':Vec2(0,5)}),
            (DoubleSpiralEnnemy,{'position':Vec2(5,5)}),
            (QuadrupleSpiralEnnemy,{'position':Vec2(10,5)}),
            (AimerEnnemy,{'position':Vec2(-10,5)}),
            (PatrolEnnemy,{'position':Vec2(0,0),'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
            (Boss1,{'position':Vec2(0,-5),'waypoints':[Vec2(-10,-5),Vec2(10,-5)],'lives':20}),
            (LaserEnnemy,{'position':Vec2(0,10)})
            
        ],
        10,
        {
            "bullets":bullets,
            "targets":players
        }
    )


    def update():
        for bullet in bullets:
            bullet.update()
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])

    def input(key):
        if key == 'enter':
            wave.start()
    app.run()
