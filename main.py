from typing import Generic
from ursina import *
from random import *
from ursina import entity
import time
#import first person controller
from ursina.prefabs.first_person_controller import FirstPersonController

class playerVar:

    speedvar = 10
    jumpLen = .5
    JumpHeight = 3




def update():
    #This code senses collisions for the player
    hit_info = player.intersects()
    if hit_info.hit:
        if hit_info.entity == target:
            text = Text(text = 'YOU LOSE', origin=(0,0), background = True)
            global finish_time
            finish_time = time.time()
            timefunc()
            application.pause()
            mouse.locked = False

        if hit_info.entity.color == color.gray.tint(0):
            player.gravity = -0.5
            anti_gravity()

        if hit_info.entity.color == color.green.tint(0):
            global start_time
            start_time = time.time()





    if held_keys['escape']:
        application.pause()
        mouse.locked = False
        inventory = Inventory()

def input(key):
    if key == 'shift':
        player.speed = playerVar.speedvar + 10
    elif key == 'shift up':
        player.speed = playerVar.speedvar
    if key == 'f':
        player.gravity = player.gravity - 2
    if key == 'f up':
        player.gravity = player.gravity + 2


def resume():
            application.resume()
            mouse.locked = False

class Inventory(Entity):

    def __init__(self):
        ReturnButton = Button(text='Return To Game', color=color.white, icon='play', scale=(0.5, 0.3) )
        ReturnButton.on_click = resume()
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (1.5, .8),
            origin = (-.2, .5),
            position = (-.3,.4),
            color = color.dark_gray
)



class blocks:
    Generic_platform = Entity(
        model='cube',
        collider='cube',
        scale=(2,1,3),
        position=(-49,2,-49),
        color=color.gray.tint(0)
    )

    Timer_start = Entity(
        model='cube',
        collider='cube',
        scale=(2,1,3),
        position=(-48,2,-48),
        color=color.green.tint(0)


    )

def anti_gravity():
    player.gravity = 0.3
    if not player.grounded:
            return

    player.grounded = False
    player.animate_y(player.y+player.jump_height, player.jump_duration, resolution=int(5//time.dt), curve=curve.out_expo)
    invoke(player.start_fall, delay=player.jump_duration)

def timefunc():
    global result_time
    result_time = (finish_time - start_time)
    show_time = Text(text = result_time, origin=(0,1), background = True)






if __name__ == '__main__':
  app = Ursina()


  #create a plane (ground to walk on)
  ground = Entity(model = 'cube',
                  scale = (100,2,100),
                  texture = 'white_cube',
                  color = color.white.tint(-0.3),
                  collider = 'box',
                  texture_scale = (50,50))

  #Create a First Person Controller and place it in the corner of the map
  player = FirstPersonController(collider ='box', model = 'cube', height = 3, speed = playerVar.speedvar, y=5, position = (-40,4,-40), jump_duration = playerVar.jumpLen, jump_height = playerVar.JumpHeight, air_time = -.5, gravity = 1.1)
  def playercontrol():
      camera.z += held_keys["w"]

  #create a lime green target cube at a random location
  target = Entity(model = 'cube',
                  scale = (2,2,2),
                  position = (49,2,49),
                  collider = 'box',
                  color = color.green)


  sky = Sky()
  app.run()
