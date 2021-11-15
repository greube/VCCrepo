from ursina import *
from random import *
#import first person controller\
global gravnum
gravnum = 0

class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 15
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1.1
        self.grounded = False
        self.jump_height = 2
        self.jump_duration = .1
        self.jumping = False
        self.air_time = 0
        self.antigravjump = False

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y


    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space':
            if gravnum == 1:
                self.jump_down()
            else:
                self.jump()


    def jump(self):


        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_duration, resolution=int(5//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.jump_duration)

    def jump_down(self):


        self.grounded = False
        self.animate_y(self.y-self.jump_height, self.jump_duration, resolution=int(5//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.jump_duration)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

def update():
    global respawn_point
    #This code senses collisions for the player
    hit_info = player.intersects()

    if hit_info.hit:
        if hit_info.entity == target:
            text = Text(text = 'YOU WIN', origin=(0,0), background = True)
            application.pause()
            mouse.locked = False
            if hit_info.entity.color == color.gray.tint(0):
                print("antigrav")
                anti_gravity()
        if hit_info.entity.color == color.orange.tint(-0.2) or hit_info.entity.color == color.black.tint(-0.2):
            respawn_point = hit_info.entity.position
        elif hit_info.entity.color == color.red.tint(-0.2):
            respawn()

        if distance(player, ground) > 100:
            respawn()




def input(key):
    if key == 'shift':
        player.speed = playerVar.speedvar + 3


    elif key == 'shift up':
        player.speed = playerVar.speedvar

    if key == 'f':
        player.gravity = -0.2
        if not player.grounded:
                return
        gravnum = 1
        player.player_height = -2
        player.jump()
        invoke(player.start_fall, delay=0.1)


    if key == 'v':
        player.gravity = 1
        invoke(player.start_fall, delay=0)





def respawn():
    player.position = respawn_point
#Define player movment characteristics
class playerVar:
    speedvar = 5
    jumpLen = .4
    JumpHeight = 2
    airtime = 0.5
    playergrav = 1
    playerFov = 120





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
                  texture_scale = (100, 100),
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
                  color = color.gray.tint(0),
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

  player = FirstPersonController(collider ='box', model = 'cube', height = 3, speed = playerVar.speedvar, y=5, position = (-42,35,-43), jump_duration = playerVar.jumpLen, jump_height = playerVar.JumpHeight, air_time = playerVar.airtime, gravity = playerVar.playergrav, )

  #create a lime green target cube at a random location
  target = Entity(model = 'cube',
                  scale = (2,2,2),
                  position = (49,2,49),
                  collider = 'box',
                  color = color.green,
                  mouse_sensitivity = Vec2(37, 37))

  sky = Sky()
  app.run()
