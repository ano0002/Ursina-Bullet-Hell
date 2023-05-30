from ursina import Vec2
import math 

class Vec2(Vec2):
    def rotate(self, angle):
        angle = math.radians(angle)
        return Vec2(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))
