from ursina import *
import time

class Particle(Entity):
    def __init__(self, pos, start, maxi, length, color=color.hsv(0, 0, 0.3), curve = curve.linear_boomerang,velocity = (0,0), **kwargs):
        super().__init__(model="quad",color=color, position=pos, scale=start)
        self.maxi = maxi
        self.animate_scale(maxi, duration=length,
                           curve=curve)
        self.start = time.time()
        self.velocity = velocity
        self.length = length
        self.alive = True
        for key, value in kwargs.items():
            try :
                setattr(self, key, value)
            except :
                print(key,value)

    def update(self):
        self.position += Vec2(self.velocity[0]*time.dt,self.velocity[1]*time.dt)
        if time.time()-(self.length) > self.start:
            destroy(self)
            self.alive = False


class Generator(Entity):
    def __init__(self, activated=True, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.last_time = time.time()
        self.last_emit = time.time()
        self.emission_rate = 0.1
        self.length = 1
        self.velocity = (0,0)
        self.curve = curve.linear
        self.start_size = 0.01
        self.maxi_size = 0.1
        self.color = color.hsv(0, 0, 0.3)
        self.activated = activated
        for key, value in kwargs.items():
            try :
                setattr(self, key, value)
            except :
                print(key,value)
        

    def update(self):
        if time.time() - self.last_emit > 1/self.emission_rate and self.activated:
            self.last_emit = time.time()
            tempvel = list(self.velocity)
            if callable(self.velocity[0]):
                tempvel[0] = self.velocity[0]()
            if callable(self.velocity[1]):
                tempvel[1] = self.velocity[1]()
            self.particles.append(Particle(self.position, self.start_size, self.start_size, self.length, self.color, self.curve, tempvel, scale=self.size))
        self.particles = [particle for particle in self.particles if particle.alive]

    @property
    def alive(self):
        return len(self.particles) > 0 or time.time()-self.last_time < self.length

    def start(self):
        self.last_time = time.time()
        self.activated = True
    
    def stop(self):
        self.activated = False
    
    def toggle(self):
        self.activated = not self.activated

    def reset(self):
        self.last_time = time.time()
        for particle in self.particles:
            destroy(particle)
        self.particles = []
        

if __name__ == "__main__":
    
    app = Ursina()
    camera.orthographic = True
    camera.fov = 32
    
    Entity(model='sphere', color=color.yellow, position=Vec2(16*camera.aspect_ratio,0))
    generator = Generator(position=Vec2(0,0), emission_rate=100,
                          length=1, velocity=(lambda : random.random()*2-1, lambda : random.random()*2 -1), 
                          curve=curve.linear_boomerang, start_size=.1, maxi_size=1, color=color.red, size=0.01)

    def input(key):
        if key == "space":
            generator.reset()
            generator.toggle()
    
    app.run()
    