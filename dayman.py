### attempt at singing swish swish

import sys
import time
import asyncio

import random

##import BlinkyCube

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo

DanceMambo = cozmo.anim.Triggers.DanceMambo

Surprise = cozmo.anim.Triggers.Surprise


def syncThisShit(listOfActions, lastTimeOut):
    for actionIndex in range(len(listOfActions)-1):
        listOfActions[actionIndex].wait_for_completed()
    listOfActions[-1].wait_for_completed(lastTimeOut)

def harmony(ourRobot):
    ourRobot.move_lift(0.70)
    ourRobot.say_text("ah", play_excited_animation=True, duration_scalar= 1, voice_pitch = .3, in_parallel = True).wait_for_completed()
    turnAngle = 360 * random.choice([-1,1])
    ourRobot.turn_in_place(cozmo.util.Angle(degrees=turnAngle), in_parallel=True, num_retries=0)
    ourRobot.say_text("ah", duration_scalar= 1, voice_pitch = .6, in_parallel = True).wait_for_completed()
    ourRobot.move_lift(-0.70)
    ourRobot.say_text("ah", duration_scalar= 1, voice_pitch = .9, in_parallel = True).wait_for_completed()
##    lift_action = ourRobot.set_lift_height(0.0, in_parallel = True, duration = 0, num_retries= 5)
##    lift_action.wait_for_completed()


def get_in_position(robot: cozmo.robot.Robot):
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face'''
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
        with robot.perform_off_charger():
            lift_action = robot.set_lift_height(0.0, in_parallel=True)
            head_action = robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE,
                                               in_parallel=True)
            lift_action.wait_for_completed()
            head_action.wait_for_completed()

def calc_pixel_threshold(image: Image):
    '''Calculate a pixel threshold based on the image.

    Anything brighter than this will be shown on (light blue).
    Anything darker will be shown off (black).
    '''

    # Convert image to gray scale
    grayscale_image = image.convert('L')

    # Calculate the mean (average) value
    mean_value = np.mean(grayscale_image.getdata())
    return mean_value



def singDayman(robot: cozmo.robot.Robot):
    get_in_position(robot)

    # load some images and convert them for display cozmo's face
    image_settings = [("images/sun.png", Image.NEAREST),
                      ("images/nightman.png", Image.NEAREST), ("images/hearts.png", Image.NEAREST)]

    face_images = []
    for image_name, resampling_mode in image_settings:
        image = Image.open(image_name)

        # resize to fit on Cozmo's face screen
        resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)

        # convert the image to the format used by the oled screen
        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image,
                                                                 invert_image=True)
        face_images.append(face_image)

        
    # getting formatted images out
    sunImg = face_images[0]
    nightManImg = face_images[1]
    heartsImg = face_images[2]


    robot.say_text("day man", duration_scalar= .5,in_parallel=True).wait_for_completed()
        
##    robot.play_anim_trigger(Surprise).wait_for_completed()
    harmony(robot)
    
    a1 = robot.say_text("fighter of the night man", duration_scalar= .7,in_parallel=True)
    a2 = robot.display_oled_face_image(nightManImg, .5 * 1000.0, in_parallel=True)

    syncThisShit([a1,a2], 0 )

    harmony(robot)
    
    a3 = robot.say_text("champion of the sun", duration_scalar= .7,in_parallel=True)
    a4 = robot.display_oled_face_image(sunImg, .5 * 1000.0, in_parallel=True)

    syncThisShit([a3,a4], 0 )

    harmony(robot)

    a5 = robot.say_text("master of karate and friendship for everyone!", duration_scalar= .7,in_parallel=True)
    a6 = robot.display_oled_face_image(heartsImg, 1.5 * 1000.0, in_parallel=True)

    syncThisShit([a5,a6], 0 )

    
##    robot.set_all_backpack_lights(cozmo.lights.red_light)


##    robot.set_all_backpack_lights(cozmo.lights.off)
    
##    robot.play_anim_trigger(DanceMambo).wait_for_completed()


cozmo.run_program(singDayman)
