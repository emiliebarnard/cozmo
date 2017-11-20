### attempt at singing swish swish

import sys
import time
import asyncio

import BlinkyCube

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo

DanceMambo = cozmo.anim.Triggers.DanceMambo

def syncThisShit(listOfActions, lastTimeOut):
    for actionIndex in range(len(listOfActions)-1):
        listOfActions[actionIndex].wait_for_completed()
    listOfActions[-1].wait_for_completed(lastTimeOut)



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



def singSwish(robot: cozmo.robot.Robot):
    get_in_position(robot)

    # load some images and convert them for display cozmo's face
    image_settings = [("images/swish.png", Image.BICUBIC),
                      ("images/bish.png", Image.NEAREST)]

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
    swishImg = face_images[0]
    bishImg = face_images[1]

    robot.say_text("wat uppppp").wait_for_completed()


    a1 = robot.say_text("swish swish", False, True, .5,in_parallel=True)
    a2 = robot.display_oled_face_image(swishImg, .5 * 1000.0, in_parallel=True)

    syncThisShit([a1,a2], 0 )

    
    robot.set_all_backpack_lights(cozmo.lights.red_light)
    a3 = robot.display_oled_face_image(bishImg, 1 * 1000.0, in_parallel=True)
    a4 = robot.say_text("bish", False, True, .5, in_parallel=True)
    


    syncThisShit([a3,a4], 0)
    robot.set_all_backpack_lights(cozmo.lights.off)
    
    robot.move_lift(0.70)
    robot.say_text("another one in the basket", False, True, .6).wait_for_completed(0)
    robot.play_anim_trigger(DanceMambo).wait_for_completed()

cozmo.run_program(singSwish)
