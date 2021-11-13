from ursina import *
from random import *
#import first person controller
from ursina.prefabs.first_person_controller import FirstPersonController

def update():
    global respawn_point
    #This code senses collisions for the player
    hit_info = player.intersects()
    
    if hit_info.hit:
        if hit_info.entity == target:
            text = Text(text = 'YOU WIN', origin=(0,0), background = True)
            application.pause()
            mouse.locked = False
        if hit_info.entity.color == color.orange.tint(-0.2) or hit_info.entity.color == color.black.tint(-0.2):
            respawn_point = hit_info.entity.position 
        elif hit_info.entity.color == color.red.tint(-0.2):
            respawn()            


    if distance(player, ground) > 100:
        respawn()
    
def respawn():
    player.position = respawn_point


if __name__ == '__main__':
  app = Ursina()

  #create a mold
  ground = Entity(model = 'cube',
                  scale = (100,2,100),
                  texture = 'white_cube',
                  color = color.red.tint(-0.2),
                  collider = 'box',
                  texture_scale = (100,100))

  ceiling = Entity(model = 'cube',
                  scale = (100,2,100),
                  texture = 'white_cube',
                  color = color.red.tint(-0.2),
                  collider = 'box',
                  texture_scale = (100,100),
                  position = (0,80, 0))

  #pc
  platform_checkpoint = Entity(model = 'cube',
                  scale = (3,1,3),
                  texture = 'white_cube',
                  color = color.orange.tint(-0.2),
                  collider = 'box',
                  texture_scale = (1, 1),
                  position = (46,45,-43))

  #pn
  platform_normal = Entity(model = 'cube',
                  scale = (2,1,3),
                  texture = 'white_cube',
                  color = color.white.tint(-0.2),
                  collider = 'box',
                  texture_scale = (1,1),
                  position = (-36.5,35,-43))
  
  #pag
  platform_antigrav = Entity(model = 'cube',
                  scale = (2,1,3),
                  texture = 'white_cube',
                  color = color.gray.tint(-0.2),
                  collider = 'box',
                  texture_scale = (1,1),
                  position = (-8.5,45,-44))
  
  #ps
  platform_spawn = Entity(model = 'cube',
                  scale = (7,1,7),
                  texture = 'white_cube',
                  color = color.black.tint(-0.2),
                  collider = 'box',
                  texture_scale = (1,1),
                  position = (-42,35,-43))

  #Duplicate all day, every day, every night
  
  #Level 1 

  pn = duplicate(platform_normal, position = (-32.5,35,-43), rotation = (0, 0, 0))
  #pn2 = duplicate(platform_normal, position = (-28.5,35,-37), rotation = (0, 0, 0))
  pn3 = duplicate(platform_normal, position = (-28,35,-44.5), rotation = (0, 90, 0))
  pn4 = duplicate(platform_normal, position = (-22.5,35,-44), rotation = (0, 0, 0))
  pn5 = duplicate(platform_normal, position = (-17.5,35,-44), rotation = (0, 0, 0))
  pn6 = duplicate(platform_normal, position = (-11.5,35,-44), rotation = (0, 0, 0))

  pag = duplicate(platform_antigrav, position = (-5.5,45,-44), rotation = (0, 0, 0))
  pag2 = duplicate(platform_antigrav, position = (-1.5,45,-44), rotation = (0, 0, 0))
  pag3 = duplicate(platform_antigrav, position = (3.5,45,-44), rotation = (0, 0, 0))
  pag4 = duplicate(platform_antigrav, position = (9.5,45,-44), rotation = (0, 0, 0))

  pn7 = duplicate(platform_normal, position = (13.5,35,-41), rotation = (0, 0, 0))
  
  pag5 = duplicate(platform_antigrav, position = (15,45,-44.5), rotation = (0, 90, 0))
  pag6 = duplicate(platform_antigrav, position = (20.5,45,-41.5), rotation = (0, 0, 0))

  pn8 = duplicate(platform_normal, position = (24, 35,-42.5), rotation = (0, 90, 0))
  pn9 = duplicate(platform_normal, position = (28.5,35,-46), rotation = (0, 0, 0))

  pag7 = duplicate(platform_antigrav, position = (31,45,-42.5), rotation = (0, 90, 0))

  pn10 = duplicate(platform_normal, position = (37,35,-41.5), rotation = (0, 90, 0))

  pag8 = duplicate(platform_antigrav, position = (42,45,-39.5), rotation = (0, 90, 0))

  #Level 2

  pn11 = duplicate(platform_normal, position = (45.5,35,-37), rotation = (0, 0, 0))
  pn12 = duplicate(platform_normal, position = (44.5,35,-32), rotation = (0, 0, 0))
  pn13 = duplicate(platform_normal, position = (40,35,-26.5), rotation = (0, 90, 0))
  pn14 = duplicate(platform_normal, position = (35.5,35,-24), rotation = (0, 0, 0))

  pne1 = duplicate(platform_normal, position = (29,35,-24), rotation = (0, 0, 0))
  pne2 = duplicate(platform_normal, position = (23,35,-24), rotation = (0, 0, 0))

  pag9 = duplicate(platform_antigrav, position = (19,45,-26.5), rotation = (0, 90, 0))
  pag10 = duplicate(platform_antigrav, position = (15,45,-25.5), rotation = (0, 90, 0))
  pag11 = duplicate(platform_antigrav, position = (10.5,45,-24), rotation = (0, 0, 0))
  pag12 = duplicate(platform_antigrav, position = (9.5,45,-19), rotation = (0, 0, 0))

  pn15 = duplicate(platform_normal, position = (3,35,-17.5), rotation = (0, 90, 0))
  pn16 = duplicate(platform_normal, position = (0.5,35,-20), rotation = (0, 0, 0))
  pn17 = duplicate(platform_normal, position = (-6,35,-22.5), rotation = (0, 90, 0))

  pag13 = duplicate(platform_antigrav, position = (-12,45,-22.5), rotation = (0, 90, 0))
  pag14 = duplicate(platform_antigrav, position = (-18,45,-22.5), rotation = (0, 90, 0))
  pag15 = duplicate(platform_antigrav, position = (-23,45,-25.5), rotation = (0, 90, 0))

  pn18 = duplicate(platform_normal, position = (-27,35,-29.5), rotation = (0, 90, 0))
  pn19 = duplicate(platform_normal, position = (-32,35,-24.5), rotation = (0, 90, 0))

  pag14 = duplicate(platform_antigrav, position = (-32.5,45,-29), rotation = (0, 0, 0))
  pag15 = duplicate(platform_antigrav, position = (-33.5,45,-20), rotation = (0, 0, 0))

  pc1 = duplicate(platform_checkpoint, position = (-48,45,-15), rotation = (0, 0, 0))

  #Create a First Person Controller and place it in the corner of the map
  player = FirstPersonController(collider ='box', model = 'cube', speed = 5, y=5, position = (-42,35,-43))

  #create a lime green target cube at a random location
  target = Entity(model = 'cube',
                  scale = (2,2,2),
                  position = (49,2,49),
                  collider = 'box',
                  color = color.green,
                  mouse_sensitivity = Vec2(37, 37))

  sky = Sky()
  app.run()
