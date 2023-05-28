from ursina import *

class Menu(Entity):
    def __init__(self,on_start,on_quit,**kwargs):
        self.on_start = on_start
        self.on_quit = on_quit
        super().__init__(parent = camera.ui,**kwargs)

        self.background = Entity(
            model = 'quad',
            texture = 'background',
            scale = (32*camera.aspect_ratio,32),
            position = (0,0,.5),
            color = color.gray
        )
        

        self.start_button = Button(
            parent = self,
            model = 'quad',
            texture = 'assets/start_button.png',    
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.5,.25),
            position = (0,0,.1),
            on_click = self.start_game
        )
    
        self.quit_button = Button(
            parent = self,
            model = 'quad',
            texture = 'assets/quit_button.png',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.5,.25),
            position = (0,-.3,.1),
            on_click = self.quit_game
        )
        
        self.title = Text(
            parent = self,
            text = 'Ursina Bullet Hell',
            origin = (0,0),
            scale = 2,
            position = (0,.3,.1)
        )
        
        self.version = Text(
            parent = self,
            text = 'v0.6',
            origin = (0,0),
            scale = 1,
            position = (0,.25,.1)
        )
        
        self.author = Text(
            parent = self,
            text = 'by @ano002',
            origin = (0,0),
            scale = 1,
            position = (.8,-.48,.1)
        )

    def start_game(self):
        destroy(self)
        destroy(self.background)
        self.on_start()
    
    def quit_game(self):
        destroy(self)
        destroy(self.background)
        self.on_quit()
    

if __name__ == '__main__':
    from shader import bullet_shader
    
    app = Ursina()
    
    camera.orthographic = True
    camera.fov = 32
    camera.shader = bullet_shader
    
    
    def on_start():
        print('start')
    def on_quit():
        application.quit()
    
    
    
    menu = Menu(on_start,on_quit)
    
    app.run()