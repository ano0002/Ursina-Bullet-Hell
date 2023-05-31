from ursina import *

class StartMenu(Entity):
    def __init__(self,on_start,on_quit,**kwargs):
        self.on_start = on_start
        self.on_quit = on_quit
        self.font = "assets/Evil Empire.otf"
        
        
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
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,0,.1),
            on_click = self.start_game,
            text="START",
            text_color = color.black,
            
        )
        self.start_button.text_entity.font = self.font
        self.start_button.text_entity.scale = 0.5        
    
        self.quit_button = Button(
            parent = self,
            model = 'quad',
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,-.3,.1),
            on_click = self.quit_game,
            text="QUIT",
            text_color = color.black
        )
        
        self.quit_button.text_entity.font = self.font
        self.quit_button.text_entity.scale = 0.5    
         
        self.title = Text(
            parent = self,
            text = 'Ursina Bullet Hell',
            font=self.font,
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
        self.selected = 0

        self.buttons = [self.start_button,self.quit_button]
        
        self.total_time = 0
        self.last_move = float('-inf')
        

    def start_game(self):
        self.background.disable()
        self.disable()
        self.on_start()
    
    def quit_game(self):
        destroy(self)
        destroy(self.background)
        self.on_quit()
    
    def input(self,key):
        if key in {"up arrow", "w","gamepad dpad up"}:
            self.selected = max((self.selected - 1),0)
        if key in {"down arrow", "s","gamepad dpad down"}:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
        if key in {"gamepad a","enter"}:
            invoke(self.buttons[self.selected].on_click,delay = 0.01)
    
    def update(self):
        self.total_time += time.dt
        
        if held_keys["gamepad left stick y"] < -.5 and time.time() - self.last_move > .2:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
            self.last_move = time.time()
        if held_keys["gamepad left stick y"] > .5 and time.time() - self.last_move > .2:
            self.selected = max((self.selected - 1),0)
            self.last_move = time.time()
        
        self.buttons[self.selected].scale = (.25,.15) + (.0125*math.sin(self.total_time*5),.0075*math.sin(self.total_time*5))
        for button in self.buttons:
            if button != self.buttons[self.selected]:
                button.scale = (.25,.15)
    
    def enable(self):
        self.background.enable()
        return super().enable()

    def disable(self):
        self.background.disable()
        return super().disable()

class PauseMenu(Entity):
    def __init__(self,on_resume,on_leave,on_quit,**kwargs):
        self.on_resume = on_resume
        self.on_leave = on_leave
        self.on_quit = on_quit
        self.font = "assets/Evil Empire.otf"
        
        
        super().__init__(parent = camera.ui,**kwargs)

        

        self.resume_button = Button(
            parent = self,
            model = 'quad',
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,.1,.1),
            on_click = self.resume_game,
            text="RESUME",
            text_color = color.black,
            
        )
        self.resume_button.text_entity.font = self.font
        self.resume_button.text_entity.scale = 0.5        
    
        self.leave_button = Button(
            parent = self,
            model = 'quad',
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,-.1,.1),
            on_click = self.leave_game,
            text="LEAVE\nGAME",
            text_color = color.black
        )
        self.leave_button.text_entity.font = self.font
        self.leave_button.text_entity.scale = 0.5
    
        self.quit_button = Button(
            parent = self,
            model = 'quad',
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,-.3,.1),
            on_click = self.quit_game,
            text="QUIT",
            text_color = color.black
        )
        self.quit_button.text_entity.font = self.font
        self.quit_button.text_entity.scale = 0.5    
         
        self.title = Text(
            parent = self,
            text = 'Ursina Bullet Hell',
            font=self.font,
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
        self.selected = 0

        self.buttons = [self.resume_button,self.leave_button,self.quit_button]
        
        self.total_time = 0
        self.destroyed = False
        self.last_move = float('-inf')

    def resume_game(self):
        self.disable()
        self.on_resume()
    
    def leave_game(self):
        self.disable()
        self.on_leave()
    
    def quit_game(self):
        self.on_quit()
    
    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    
    def input(self,key):
        if key in {"up arrow", "w","gamepad dpad up"}:
            self.selected = max((self.selected - 1),0)
        if key in {"down arrow", "s","gamepad dpad down"}:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
        if key in {"gamepad a","enter"}:
            invoke(self.buttons[self.selected].on_click,delay = 0.01)
    
    def update(self):
        self.total_time += time.dt
        
        if held_keys["gamepad left stick y"] < -.5 and time.time() - self.last_move > .2:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
            self.last_move = time.time()
        if held_keys["gamepad left stick y"] > .5 and time.time() - self.last_move > .2:
            self.selected = max((self.selected - 1),0)
            self.last_move = time.time()
        
        self.buttons[self.selected].scale = (.25,.15) + (.0125*math.sin(self.total_time*5),.0075*math.sin(self.total_time*5))
        for button in self.buttons:
            if button != self.buttons[self.selected]:
                button.scale = (.25,.15)


class PlayerCountSelection(Entity):
    def __init__(self,on_select,on_back,**kwargs):
        
        self.on_select = on_select
        self.on_back = on_back
        self.font = "assets/Evil Empire.otf"
        
        
        super().__init__(parent = camera.ui,**kwargs)

        

        self.one = Button(
            parent = self,
            model = 'quad',
            texture = 'buttonvert',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.15,.25),
            position = (-.5,0,.1),
            on_click = Func(self.on_select,1),
            text="1",
            text_color = color.black,
        )
        self.one.text_entity.font = self.font
        self.one.text_entity.scale = 0.5      
        
        
        self.two = Button(
            parent = self,
            model = 'quad',
            texture = 'buttonvert',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.15,.25),
            position = (-.16,0,.1),
            on_click = Func(self.on_select,2),
            text="2",
            text_color = color.black,
        )
        self.two.text_entity.font = self.font
        self.two.text_entity.scale = 0.5        
    
        self.three = Button(
            parent = self,
            model = 'quad',
            texture = 'buttonvert',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.15,.25),
            position = (.16,0,.1),
            on_click = Func(self.on_select,3),
            text="3",
            text_color = color.black
        )
        self.three.text_entity.font = self.font
        self.three.text_entity.scale = 0.5

        self.four = Button(
            parent = self,
            model = 'quad',
            texture = 'buttonvert',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.15,.25),
            position = (.5,0,.1),
            on_click = Func(self.on_select,4),
            text="4",
            text_color = color.black
        )
        self.four.text_entity.font = self.font
        self.four.text_entity.scale = .5
    
        self.back_button = Button(
            parent = self,
            model = 'quad',
            texture = 'button',
            color = color.white,
            highlight_color = color.gray,
            pressed_color = color.white,
            scale = (.25,.15),
            position = (0,-.3,.1),
            on_click = self.on_back,
            text="BACK",
            text_color = color.black
        )
        self.back_button.text_entity.font = self.font
        self.back_button.text_entity.scale = 0.5
    
        self.title = Text(
            parent = self,
            text = 'Ursina Bullet Hell',
            font=self.font,
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
        self.selected = 0

        self.back_selected = False

        # button list
        self.buttons = [self.one,self.two,self.three,self.four]
        
        self.total_time = 0
        self.destroyed = False
        self.last_move = float('-inf')
        
    
    def input(self,key):
        if key in {"left arrow", "a","gamepad dpad left"}:
            self.selected = max((self.selected - 1),0)
        if key in {"right arrow", "d","gamepad dpad right"}:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
        if key in {"up arrow", "w","gamepad dpad up"}:
            self.back_selected = False
        if key in {"down arrow", "s","gamepad dpad down"}:
            self.back_selected = True
        if key in {"gamepad a","enter"}:
            if self.back_selected:
                invoke(self.back_button.on_click,delay = 0.01)
            else:
                invoke(self.buttons[self.selected].on_click,delay = 0.01)
    
    def update(self):
        self.total_time += time.dt
        
        if held_keys["gamepad left stick x"] < -.5 and time.time() - self.last_move > .2:
            self.selected = max((self.selected - 1),0)
            self.last_move = time.time()
        if held_keys["gamepad left stick x"] > .5 and time.time() - self.last_move > .2:
            self.selected = min((self.selected + 1),len(self.buttons)-1)
            self.last_move = time.time()
        if held_keys["gamepad left stick y"] < -.5 and time.time() - self.last_move > .2:
            self.back_selected = True
            self.last_move = time.time()
        if held_keys["gamepad left stick y"] > .5 and time.time() - self.last_move > .2:
            self.back_selected = False
            self.last_move = time.time()
        
       
        if self.back_selected:
            self.back_button.scale = (.25,.15) + (.0075*math.sin(self.total_time*5),.0125*math.sin(self.total_time*5))
            for button in self.buttons:
                button.scale = (.15,.25)
        else:
            self.back_button.scale = (.25,.15)
            self.buttons[self.selected].scale = (.15,.25) + (.0075*math.sin(self.total_time*5),.0125*math.sin(self.total_time*5))
            for button in self.buttons:
                if button != self.buttons[self.selected]:
                    button.scale = (.15,.25)


if __name__ == '__main__':
    from shader import bullet_shader
    
    app = Ursina()
    
    camera.orthographic = True
    camera.fov = 32
    camera.shader = bullet_shader
    
    def on_start():
        print('start')
    
    def on_resume():
        print('resume')
        
    def on_leave():
        print('leave')
        
    def on_quit():
        application.quit()
    
    """
    menu = StartMenu(on_start,on_quit)
    pausemenu = PauseMenu(on_resume,on_leave,on_quit)
    
    pausemenu.disable()
    
    def input(key):
        if key == "gamepad b" :
            menu.enable()

        if key == "escape":
            pausemenu.toggle()
    """
    menu = PlayerCountSelection(on_start,on_quit)
    
    app.run()