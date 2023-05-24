from ursina import *
from player import ControllerPlayer, KeyboadPlayer
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset


app = Ursina(development_mode=True)

camera.orthographic = True
camera.fov = 32


tilemap = Tilemap("./assets/maps/map.csv",Tileset("./assets/tileset.png"))

camera.shader = bullet_shader
bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

p1 = KeyboadPlayer(bullets)
p2 = ControllerPlayer(bullets)


def update():
    for bullet in bullets:
        bullet.update()
    camera.set_shader_input("camera_position", camera.position)
    camera.set_shader_input("points", [bullet.get_position() for bullet in bullets])

app.run()