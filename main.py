import time
from fastgrab import screenshot
from pymouse import PyMouse


y_click = 1400
xs_click = [500, 1000]

screen_frame = 610, 1149, 314, 6
loose_check_pixel = 600, 1300, 1, 1
man_check_pixel = 605, 1231, 1, 1


def are_you_winning_son() -> bool:
    pix = screenshot.Screenshot().capture(bbox=loose_check_pixel).reshape(4)
    return False if pix.tolist() == [238, 178, 86, 0] else True


def where_is_man() -> int:
    pix = screenshot.Screenshot().capture(bbox=man_check_pixel).reshape(4)
    return 0 if sum(pix.tolist()) > 740 else 1


def is_similar(pair: tuple) -> bool:
    l, r = pair
    return False if abs(l[0] - r[0]) > 3 or abs(l[1] - r[1]) > 3 or abs(l[2] - r[2]) > 3 else True


if __name__ == '__main__':
    mouse = PyMouse()
    t0 = time.time()
    while True:
        print('Start waiting...')

        while not are_you_winning_son():
            pass

        while are_you_winning_son():
            position = where_is_man()

            line = screenshot.Screenshot().capture(bbox=screen_frame)[:, :, :3]
            upper_pixels = tuple(line[0, 0].tolist()), tuple(line[0, -1].tolist())
            down_pixels = tuple(line[5, 0].tolist()), tuple(line[5, -1].tolist())

            if is_similar((down_pixels[position], upper_pixels[position])):
                mouse.click(xs_click[int(position)], y_click)
            else:
                mouse.click(xs_click[int(not position)], y_click)
                mouse.click(xs_click[int(not position)], y_click)

        if time.time() - t0 < 60 * 30:
            input()
            mouse.click(600, 1500)
        else:
            print('You\'d better restart the game')
