from ursina import *
from ennemy import *
from world import World
from custom_math import Vec2

app = Ursina(development_mode=True)


waves = [
        Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (SpiralEnnemy,{'position':Vec2(0,5)}),
                (PatrolEnnemy,{'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
                (PatrolEnnemy,{'waypoints':[Vec2(10,10),Vec2(10,0),Vec2(-10,0),Vec2(-10,10)]}),
                (LaserEnnemy,{'position':Vec2(0,10)})
            ],50 ),
        Wave(
            [
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,-5)}),
                (MachineGunEnnemy,{'position':Vec2(5,5)}),
                (MachineGunEnnemy,{'position':Vec2(5,-5)})
            ],50 ),
        Wave(
            [
                (QuadrupleSpiralEnnemy,{'position':Vec2(5,5)}),
                (QuadrupleSpiralEnnemy,{'position':Vec2(-8,-11)}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)}),
                (MachineGunEnnemy,{'position':Vec2(-5,-5)}),
                (MachineGunEnnemy,{'position':Vec2(5,5)}),
                (MachineGunEnnemy,{'position':Vec2(5,-5)}),
                (PatrolEnnemy,{'waypoints':[Vec2(-10,0),Vec2(-10,10),Vec2(10,10),Vec2(10,0)]}),
                (PatrolEnnemy,{'waypoints':[Vec2(10,10),Vec2(10,0),Vec2(-10,0),Vec2(-10,10)]})
            ],50 ),
        Wave(
            [
                (Boss2,{'position':Vec2(0,-5),'waypoints':[Vec2(-10,-5),Vec2(10,-5)],'lives':20}),
                (MachineGunEnnemy,{'position':Vec2(-5,5)})
            ],90 ),
        Wave(
            [
                (LaserEnnemy,{'position':Vec2(0,0)}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":240}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":120}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":300}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":60}),
                (LaserEnnemy,{'position':Vec2(0,0),"rotation_z":180}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(0)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(72)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(144)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(216)}),
                (MachineGunEnnemy,{'position':Vec2(4,0).rotate(288)}),
            ],50 )
        ]


world = World(waves)

app.run()