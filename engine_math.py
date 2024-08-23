import math


def coord_quarter(x1, y1, x2, y2):
    if x2 > x1 and y2 < y1:
        return 1
    elif x2 < x1 and y2 < y1:
        return 2
    elif x2 < x1 and y2 > y1:
        return 3
    elif x2 > x1 and y2 > y1:
        return 4
    return 0


def calculate_angle(x1, y1, x2, y2):
    quarter = coord_quarter(x1, y1, x2, y2)
    len_x, len_y = x2 - x1, y1 - y2
    if not quarter:
        if len_y == 0 and len_x > 0:
            angle = 90
        elif len_y == 0 and len_x < 0:
            angle = 270
        elif len_x == 0 and len_y < 0:
            angle = 180
        else:
            angle = 0
    elif quarter == 1:
        angle = math.degrees(math.atan(len_x / len_y))
    elif quarter == 2:
        angle = 270 - math.degrees(math.atan(len_y / len_x))
    elif quarter == 3:
        angle = 180 + math.degrees(math.atan(len_x / len_y))
    else:
        angle = 90 - math.degrees(math.atan(len_y / len_x))
    return angle


def hypotenuse(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def convert_angle(angle):
    magic_number = 1
    while angle > 90:
        angle -= 90
        magic_number += 1
    return angle, magic_number


def change_position(angle, speed, direction):
    angle, magic_number = convert_angle(angle)
    if direction == 1:
        if magic_number == 1:
            x_speed = speed * math.sin(math.radians(angle))
            y_speed = -speed * math.cos(math.radians(angle))
        elif magic_number == 4:
            x_speed = -speed * math.cos(math.radians(angle))
            y_speed = -speed * math.sin(math.radians(angle))
        elif magic_number == 3:
            x_speed = -speed * math.sin(math.radians(angle))
            y_speed = speed * math.cos(math.radians(angle))
        else:
            x_speed = speed * math.cos(math.radians(angle))
            y_speed = speed * math.sin(math.radians(angle))
    # elif direction == 2:
    #     if magic_number == 1:
    #         x_speed = int(-speed * math.sin(math.radians(angle)))
    #         y_speed = int(-speed * math.cos(math.radians(angle)))
    #     elif magic_number == 4:
    #         x_speed = int(speed * math.cos(math.radians(angle)))
    #         y_speed = int(-speed * math.sin(math.radians(angle)))
    #     elif magic_number == 3:
    #         x_speed = int(speed * math.sin(math.radians(angle)))
    #         y_speed = int(speed * math.cos(math.radians(angle)))
    #     else:
    #         x_speed = int(-speed * math.cos(math.radians(angle)))
    #         y_speed = int(speed * math.sin(math.radians(angle)))
    # elif direction == 3:
    #     if magic_number == 1:
    #         x_speed = int(-speed * math.sin(math.radians(90 - angle)))
    #         y_speed = int(speed * math.cos(math.radians(90 - angle)))
    #     elif magic_number == 4:
    #         x_speed = int(-speed * math.cos(math.radians(90 - angle)))
    #         y_speed = int(-speed * math.sin(math.radians(90 - angle)))
    #     elif magic_number == 3:
    #         x_speed = int(-speed * math.sin(math.radians(90 - angle)))
    #         y_speed = int(-speed * math.cos(math.radians(90 - angle)))
    #     else:
    #         x_speed = int(speed * math.sin(math.radians(90 - angle)))
    #         y_speed = int(speed * math.cos(math.radians(90 - angle)))
    # else:
    #     if magic_number == 1:
    #         x_speed = int(speed * math.cos(math.radians(angle)))
    #         y_speed = int(-speed * math.sin(math.radians(angle)))
    #     elif magic_number == 4:
    #         x_speed = int(speed * math.sin(math.radians(angle)))
    #         y_speed = int(-speed * math.cos(math.radians(angle)))
    #     elif magic_number == 3:
    #         x_speed = int(-speed * math.cos(math.radians(angle)))
    #         y_speed = int(-speed * math.sin(math.radians(angle)))
    #     else:
    #         x_speed = int(-speed * math.sin(math.radians(angle)))
    #         y_speed = int(-speed * math.cos(math.radians(angle)))
    return x_speed, y_speed
