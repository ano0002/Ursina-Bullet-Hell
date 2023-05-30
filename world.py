from ursina import *
from player import Player
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from menu import StartMenu, PauseMenu
from ennemy import *

app = Ursina(development_mode=True)

camera.orthographic = True
camera.fov = 32

class World(Entity):
    def __init__(self,waves):
        super().__init__()
        self.waves = waves
        for index,wave in enumerate(waves[:-1]):
            wave.next_wave = waves[index+1]
    
        self.tileset = Tileset("./assets/tileset.png")
        self.tilemap = Tilemap("./assets/maps/map.csv",self.tileset)
        self.tilemap.disable()

        camera.shader = bullet_shader
        self.bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

        p1 = Player(self.bullets, controls={"up":"gamepad left stick y",
                                "down":"",
                                "right":"gamepad left stick x",
                                "left":"",
                                "shoot":"gamepad a",
                                "dash":"gamepad start"},
                                left = True)
        p2 = Player(self.bullets)

        self.players = [p1,p2]

        for player in self.players:
            player.disable()
            player.world = self
            
        for wave in self.waves :
            wave.args = {
                "bullets":self.bullets,
                "targets":self.players
            }
            wave.world = self

        self.paused = False
        self.playing = False
    
        self.pause_menu = PauseMenu(on_resume=self.on_resume,on_leave=self.on_leave,on_quit=application.quit)
        self.pause_menu.disable()
        
        self.start_menu = StartMenu(on_start=self.start_game,on_quit=application.quit)


    def update(self):
        if self.playing :
            if not self.paused:
                for bullet in self.bullets:
                    bullet.update()
                camera.set_shader_input("camera_position", camera.position)
                camera.set_shader_input("points", [bullet.get_position() for bullet in self.bullets])
    
    def start_game(self):
        for player in self.players:
            player.enable()
        self.waves[0].start()
        self.tilemap.enable()
        self.playing = True
    

        
    def on_leave(self):
        self.paused = False
        for bullet in bullets:
            bullet.available = True
        self.start_menu.enable()

    def toggle_pause(self):
        self.paused = not self.paused

    def on_pause(self):
        self.paused = True
        
    def on_resume(self):
        self.paused = False
        
    
    def input(self,key):
        if key in {"escape", "gamepad b"}:
            self.pause_menu.toggle()
            self.toggle_pause()
            
    