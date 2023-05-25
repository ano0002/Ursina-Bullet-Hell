from ursina import *
from player import ControllerPlayer, KeyboadPlayer
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from ennemy import *

app = Ursina(development_mode=True)

camera.orthographic = True
camera.fov = 32


tileset = Tileset("./assets/tileset.png")
tilemap = Tilemap("./assets/maps/map.csv",tileset)

camera.shader = bullet_shader
bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

p1 = KeyboadPlayer(bullets)
p2 = ControllerPlayer(bullets)

players = [p1,p2]

waves = [Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],3 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (SpiralEnnemy,{'position':Vec2(0,5)}),
                (PatrolEnnemy,{'position':Vec2(0,0),'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
                (LaserEnnemy,{'position':Vec2(0,10)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (DoubleSpiralEnnemy,{'position':Vec2(5,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (QuadrupleSpiralEnnemy,{'position':Vec2(10,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (AimerEnnemy,{'position':Vec2(-10,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            }),
        Wave(
            [
                (Boss1,{'position':Vec2(0,-5),'waypoints':[Vec2(-10,-5),Vec2(10,-5)],'lives':50}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],50 ,{
                "bullets":bullets,
                "targets":players
            })
        ]

for index,wave in enumerate(waves[:-1]):
    wave.next_wave = waves[index+1]

def update():
    for bullet in bullets:
        bullet.update()
    camera.set_shader_input("camera_position", camera.position)
    camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])

def input(key):
    if key == 'enter':
        waves[0].start()

app.run()