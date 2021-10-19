from ursina import *
from random import *
#import first person controller
from ursina.prefabs.first_person_controller import FirstPersonController


def update():
    #This code senses collisions for the player
    hit_info = player.intersects()
    if hit_info.hit:
        if hit_info.entity == target:
            text = Text(text = 'YOU LOSE', origin=(0,0), background = True)
            application.pause()
            mouse.locked = False

    if held_keys['escape']:
        application.pause()
        mouse.locked = False
        inventory = Inventory()


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


if __name__ == '__main__':
  app = Ursina()

  #create a plane (ground to walk on)
  ground = Entity(model = 'cube',
                  scale = (100,2,100),
                  texture = 'white_cube',
                  color = color.white.tint(-0.2),
                  collider = 'box',
                  texture_scale = (50,50))

  #Create a First Person Controller and place it in the corner of the map
  player = FirstPersonController(collider ='box', model = 'cube', speed = 5, y=5, position = (-40,4,-40))

  #create a lime green target cube at a random location
  target = Entity(model = 'cube',
                  scale = (2,2,2),
                  position = (49,2,49),
                  collider = 'box',
                  color = color.green)


  sky = Sky()
  app.run()
