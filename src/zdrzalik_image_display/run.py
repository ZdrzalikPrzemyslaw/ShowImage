from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import screen_brightness_control as sbc
import screeninfo

window_name = 'projector'

def get_time_now():
    return datetime.now().strftime("%I:%M:%S")


def display_image(time_black_screen=5000, time_white_screen=4000):
    date = datetime.now().strftime("%Y_%m_%d")
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height
    current_brightness = sbc.get_brightness()
    f = open(date + "/times.txt", "a")

    Path(date).mkdir(parents=True, exist_ok=True)
    time = get_time_now()
    f.write("Start " + time + "\n")

    sbc.set_brightness(0, display=0, force=True)
    image = np.zeros((height, width, 3), dtype=np.float32)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, image)
    time = get_time_now()
    f.write("Display Black " + time + "\n")
    k = cv2.waitKey(time_black_screen)

    image = np.ones((height, width, 3), dtype=np.float32)
    cv2.imshow(window_name, image)
    time = get_time_now()
    f.write("Display White " + time + "\n")
    sbc.set_brightness(100, display=0, force=True)
    k = cv2.waitKey(time_white_screen)
    cv2.destroyAllWindows()

    sbc.set_brightness(current_brightness, display=0, force=True)

    time = datetime.now().strftime("%I:%M:%S")
    f.write("End " + time + "\n")
    f.close()


def __main():
    display_image()


if __name__ == '__main__':
    __main()
