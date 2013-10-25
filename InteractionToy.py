#Code by Ian Ford
import sys, math, random, time
from pyglet.gl import *
from pyglet.window import *

window = pyglet.window.Window(800,600)
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

#Sounds accredited to http://soundbible.com/
jumpSound = pyglet.resource.media('jump.wav', streaming = False)
jumpSound.play()
pyglet.resource.media('bgmus.wav', streaming = False).play()

tex1 = pyglet.image.load('bd.png').get_texture()
tex2 = pyglet.image.load('character.png').get_texture()
tex3 = pyglet.image.load('cloud.png').get_texture()
tex4 = pyglet.image.load('key.png').get_texture()
tex5 = pyglet.image.load('sun.png').get_texture()

x = 0 #CHARACTER MOVEMENT VARS
y = 0

cloudx = 800 #CLOUD 1 MOVEMENT VAR
cloudx2 = 1400 #CLOUD 2 MOVEMENT VAR

keyCheck = True
jump = False

bdArray = [0,0, 800,0, 0,600, 800,600]
chArray = [0,66, 111,66, 0,tex2.height+66, 111,tex2.height+66]
clArray = [0,300, tex3.width,300, 0,tex3.height+300, tex3.width,tex3.height+300]
kyArray = [700,100, 800,100, 700,200, 800,200]
suArray = [250,450, 550,450, 250,750, 550,750]

bg = pyglet.graphics.vertex_list(4, ('v2f', bdArray), ('t2f', [0,0, 1,0, 0,1, 1,1]))
ch = pyglet.graphics.vertex_list(4, ('v2f', chArray), ('t2f', [0,0, 1,0, 0,1, 1,1]))
cl = pyglet.graphics.vertex_list(4, ('v2f', clArray), ('t2f', [0,0, 1,0, 0,1, 1,1]))
ky = pyglet.graphics.vertex_list(4, ('v2f', kyArray), ('t2f', [0,0, 1,0, 0,1, 1,1]))
su = pyglet.graphics.vertex_list(4, ('v2f', suArray), ('t2f', [0,0, 1,0, 0,1, 1,1]))

@window.event
def on_draw():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)

    if not keyCheck:
        glColor4f(0.4,0.3,0.6,0.4)

    #BACKGROUND
    glBindTexture(GL_TEXTURE_2D, tex1.id)
    bg.draw(GL_TRIANGLE_STRIP)

    #SUN
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, tex5.id)
    su.draw(GL_TRIANGLE_STRIP)
    glPopMatrix()

    #CLOUDS

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, tex3.id)
    
    glTranslatef(cloudx,100,0) #CLOUD 1
    cl.draw(GL_TRIANGLE_STRIP)
    glTranslatef(-cloudx,-100,0)

    glTranslatef(cloudx2,-50,0) #CLOUD 2
    cl.draw(GL_TRIANGLE_STRIP)
    glTranslatef(-cloudx2,50,0)
    glDisable(GL_BLEND)

    #KEY
    glBindTexture(GL_TEXTURE_2D, tex4.id)
    if keyCheck:
        ky.draw(GL_TRIANGLE_STRIP)
    if not keyCheck:
        glTranslatef(-700,0,0)
        ky.draw(GL_TRIANGLE_STRIP)
        glTranslatef(700,0,0)

    #CHARACTER
    glPushMatrix()
    glEnable(GL_BLEND)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, tex2.id)
    glTranslatef(x,-10+y,0) #-10 is to align the character on the 'ground'
    ch.draw(GL_TRIANGLE_STRIP)
    
    glDisable(GL_BLEND)
    glPopMatrix()

    glColor4f(1.0,1.0,1.0,1.0)
    glDisable(GL_TEXTURE_2D)

up = True

def update(dt):
    global cloudx, cloudx2, x, y, keyCheck, jump, startTime, up, sunr

    #JUMP
    if jump:
        if up:
            y += 4.81
        if not up:
            y -= 4.81
        if y >= 60:
            up = False;
            y = 60
        if y <= 0:
            jump = False
            y = 0

    #KEY IS TOUCHED!
    if x >= 680:
        keyCheck = False

    #KEY IS BROUGHT BACK
    if not keyCheck:
        if x <= 30:
            keyCheck = True

    #CLOUD MOVEMENT
    if keyCheck:
        if cloudx >= (0 - tex2.width - 100):
            cloudx -= 1
        if cloudx < (0 - tex2.width - 100):
            cloudx = 800
        if cloudx2 >= (0 - tex2.width - 100):
            cloudx2 -= 1.4
        if cloudx2 < (0 - tex2.width - 100):
            cloudx2 = 1400
        
    #KEYBOARD INPUT HANDLER
    if keyboard[pyglet.window.key.RIGHT]:
        if x < (800-111):
            x += 1
            x += 1
            x += 1
            x += 1
    if keyboard[pyglet.window.key.LEFT]:
        if x > 0:
            x -= 1
            x -= 1
            x -= 1
            x -= 1
    if keyboard[pyglet.window.key.SPACE]:
        if not jump:
            jumpSound.play()
            jump = True
            up = True

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()
