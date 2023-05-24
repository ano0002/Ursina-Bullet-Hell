from ursina import *
from player import ControllerPlayer, KeyboadPlayer
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from ennemy import SpiralEnnemy

app = Ursina(development_mode=True)

camera.orthographic = True
camera.fov = 32


tileset = Tileset("./assets/tileset.png")
tilemap = Tilemap("./assets/maps/map.csv",tileset)

camera.shader = bullet_shader
bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

p1 = KeyboadPlayer(bullets)
p2 = ControllerPlayer(bullets)

ennemy = SpiralEnnemy(bullets, position=Vec2(5,5))

def update():
    for bullet in bullets:
        bullet.update()
    camera.set_shader_input("camera_position", camera.position)
    camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])

app.run()