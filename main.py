from ursina import *
from player import ControllerPlayer, KeyboadPlayer
from shader import bullet_shader

app = Ursina()

camera.orthographic = True
camera.fov = 32

camera.shader = bullet_shader
p1 = KeyboadPlayer()
p2 = ControllerPlayer()

bullets = [Vec2(0,1) for _ in range(100)]

def update():
    for bullet in bullets:
        bullet += Vec2(time.dt) 
    camera.set_shader_input("camera_position", camera.position)
    camera.set_shader_input("points", bullets)

app.run()