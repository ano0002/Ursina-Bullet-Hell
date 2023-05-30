from ursina import *
from player import Player
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from menu import StartMenu, PauseMenu
from ennemy import *

app = Ursina(development_mode=True)

class Vec2(Vec2):
    def rotate(self, angle):
        angle = math.radians(angle)
        return Vec2(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))

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
                                left = True)
p2 = Player(bullets)

players = [p1,p2]

waves = [
        Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,-5)}),
                (MachineGunEnnemy,{'position':Vec2(5,5)}),
                (MachineGunEnnemy,{'position':Vec2(5,-5)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (SpiralEnnemy,{'position':Vec2(0,5)}),
                (PatrolEnnemy,{'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
                (PatrolEnnemy,{'waypoints':[Vec2(10,10),Vec2(10,0),Vec2(-10,0),Vec2(-10,10)]}),
                (LaserEnnemy,{'position':Vec2(0,10)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (QuadrupleSpiralEnnemy,{'position':Vec2(5,5)}),
                (QuadrupleSpiralEnnemy,{'position':Vec2(-8,-11)}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,-5)}),
                (MachineGunEnnemy,{'position':Vec2(5,5)}),
                (MachineGunEnnemy,{'position':Vec2(5,-5)}),
                (PatrolEnnemy,{'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
                (PatrolEnnemy,{'waypoints':[Vec2(10,10),Vec2(10,0),Vec2(-10,0),Vec2(-10,10)]})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (Boss2,{'position':Vec2(0,-5),'waypoints':[Vec2(-10,-5),Vec2(10,-5)],'lives':20}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],90 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (LaserEnnemy,{'position':Vec2(0,0)}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":240}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":120}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":300}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":60}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":180}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(0)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(72)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(144)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(216)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(288)}),
            ],50 ,{
                "bullets":bullets,
                "targets":players
            })
        ]

for index,wave in enumerate(waves[:-1]):
    wave.next_wave = waves[index+1]

for player in players:
    player.disable()

tilemap.disable()

def update():
    for bullet in bullets:
        bullet.update()
    camera.set_shader_input("camera_position", camera.position)
    camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])
    
def on_start():
    for player in players:
        player.enable()
    waves[0].start()
    tilemap.enable()

def on_resume():
    global paused
    paused = False
    
def on_leave():
    global paused,bullets,start_menu
    paused = False
    for entity in scene.entities:
        destroy(entity)
    for bullet in bullets:
        bullet.available = True
    start_menu = StartMenu(on_start=on_start,on_quit=application.quit)
    

pause_menu = PauseMenu(on_resume=on_resume,on_leave=on_leave,on_quit=application.quit)
pause_menu.disable()

def input(key):
    if key == "escape":
        if start_menu.destroyed:
            pause_menu.toggle()
    if key == "f11":
        window.fullscreen = not window.fullscreen

start_menu = StartMenu(on_start=on_start,on_quit=application.quit)

app.run()