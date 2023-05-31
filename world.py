from ursina import *
from player import Player
from shader import bullet_shader
from bullet import Bullet
from tilemap import Tilemap, Tileset
from menu import StartMenu, PauseMenu, PlayerCountSelection
from ennemy import *
from copy import deepcopy


class World(Entity):
    def __init__(self,waves : list[Wave]):
        super().__init__()
        self.waves = waves
        for index,wave in enumerate(waves[:-1]):
            wave.next_wave = waves[index+1]
    

        self.original_waves = deepcopy(waves)

        camera.orthographic = True
        camera.fov = 32
        camera.shader = bullet_shader
        self.bullets = [Bullet(Vec2(1,1),Vec2(0,0)) for _ in range(1000)]

        self.pause_menu = PauseMenu(on_resume=self.on_resume,on_leave=self.on_leave,on_quit=application.quit)
        self.pause_menu.disable()
    
        self.player_count_selection = PlayerCountSelection(on_select=self.on_player_count_selected,on_back=self.back_to_home)
        self.player_count_selection.disable()
        
        self.reset()
        
    def back_to_home(self):
        self.player_count_selection.disable()
        self.pause_menu.disable()
        self.start_menu.enable()
        self.status = "main_menu"

    def on_player_count_selected(self,player_count : int):
        self.player_count_selection.disable()
        for i in range(player_count):
            self.players[i].enable()
        self.waves[0].start()
        self.tilemap.enable()
        self.status = "playing"
    
    def initialize_map(self):
        self.tileset = Tileset("./assets/tileset.png")
        self.tilemap = Tilemap("./assets/maps/map.csv",self.tileset)
        self.tilemap.disable()
    
    def reset(self):
        self.initialize_map()
        p2 = Player(self.bullets, controls={"up":"gamepad left stick y",
                                "down":"",
                                "right":"gamepad left stick x",
                                "left":"",
                                "shoot":"gamepad a",
                                "dash":"gamepad start"},
                                left = True)
        
        p1 = Player(self.bullets)
        
        p3 = Player(self.bullets, controls={"up":"up arrow",
                                "down":"down arrow",
                                "right":"right arrow",
                                "left":"left arrow",
                                "shoot":"enter",
                                "dash":"0"},
                                left = True,
                                bottom = True)
        
        p4 = Player(self.bullets, controls={"up":"gamepad_1 left stick y",
                                "down":"",
                                "right":"gamepad_1 left stick x",
                                "left":"",
                                "shoot":"gamepad_1 a",
                                "dash":"gamepad_1 start"},
                                bottom = True)
        
        self.players = [p1,p2,p3,p4]

        for player in self.players:
            player.disable()
            player.world = self
            
        for wave in self.waves :
            wave.args = {
                "bullets":self.bullets,
                "targets":self.players
            }
            wave.world = self
    
        self.status = "main_menu"
        
        self.start_menu = StartMenu(on_start=self.start_game,on_quit=application.quit)

    @property
    def alive_players(self):
        return [player for player in self.players if not player.disabled]

    @property
    def playing(self):
        return self.status in {"playing","paused"}

    @playing.setter
    def playing(self,value : bool):
        if value :
            self.status = "playing"

    def update(self):
        if self.playing :
            if not self.status == "paused":
                for bullet in self.bullets:
                    bullet.update()
        camera.set_shader_input("camera_position", camera.position)
        camera.set_shader_input("points", [bullet.get_position() for bullet in self.bullets])
    
    def start_game(self):
        self.status = "player_count_selection"
        self.player_count_selection.enable()
    

        
    def on_leave(self):
        self.status = "main_menu"
        for bullet in self.bullets:
            bullet.disable()
        for player in self.players:
            destroy(player)
            for heart in player.heart_containers:
                destroy(heart)
        destroy(self.tilemap)
        ennemies = []   
        for wave in self.waves:
            ennemies.extend(wave.spawned)
        for ennemy in ennemies:
            destroy(ennemy)
        destroy(self.start_menu)
        self.waves = deepcopy(self.original_waves)
        for child in self.start_menu.children:
            destroy(child)
        destroy(self.start_menu)
        self.reset()

    def toggle_pause(self):
        if self.status == "paused":
            self.status = "playing"
        else :
            self.status = "paused"

    def on_pause(self):
        self.status = "paused"
        
    def on_resume(self):
        self.status = "playing"
        
    
    def input(self,key : str):
        if self.playing :
            if key in {"escape", "gamepad b"}:
                self.pause_menu.toggle()
                self.toggle_pause()
            
    