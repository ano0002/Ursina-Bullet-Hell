from ursina import *
import random


bullet_shader = Shader(fragment=open("bullet.frag").read(),
default_input={
    "points" : [Vec3(0,0,random.randint(0,1)) for _ in range(1000)],
    "team1_color" : Vec4(0,1,0,1),
    "team2_color" : Vec4(1,0,0,1),
    "camera_position" : Vec3(0,0,0),
    "bullets_size" : 0.01
})

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    e = Entity(model='sphere', color=color.yellow)#,scale = 0.4)
    e = Entity(model='cube', y=-1)
    camera.shader = bullet_shader

    def update():
        if held_keys["a"]:
            camera.x -= 4 * time.dt
        if held_keys["d"]:
            camera.x += 4 * time.dt
        if held_keys["w"]:
            camera.y += 4 * time.dt
        if held_keys["s"]:
            camera.y -= 4 * time.dt
        
        
        camera.set_shader_input("camera_position", camera.position)

    app.run()