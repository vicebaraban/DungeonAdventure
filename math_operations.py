import math


def coord_quarter(x1, y1, x2, y2):
    if x2 >= x1 and y2 >= y1:
        return 1
    elif x2 <= x1 and y2 >= y1:
        return 2
    elif x2 <= x1 and y2 <= y1:
        return 3
    return 4


def calculate_angle(x1, y1, x2, y2):
    quarter = coord_quarter(x1, y1, x2, y2)
    len_x, len_y = x2 - x1, y2 - y1
    if quarter == 1:
        angle = int(math.atan(math.radians(len_x / len_y)))
    elif quarter == 2:
        angle = 270 - int(math.atan(math.radians(len_x / len_y)))
    elif quarter == 3:
        angle = 180 + int(math.atan(math.radians(len_x / len_y)))
    else:
        angle = 90 - int(math.atan(math.radians(len_x / len_y)))
    return angle


def convert_angle(angle):
    magic_number = 1
    while angle > 90:
        angle -= 90
        magic_number += 1
    return angle, magic_number


def change_position(start_position, angle, speed, direction):
    angle, magic_number = convert_angle(angle)
    if direction == 1:
        if magic_number == 1:
            x_speed = int(speed * math.sin(math.radians(angle)))
            y_speed = int(speed * math.cos(math.radians(angle)))
        elif magic_number == 4:
            x_speed = int(-speed * math.cos(math.radians(angle)))
            y_speed = int(speed * math.sin(math.radians(angle)))
        elif magic_number == 3:
            x_speed = int(-speed * math.sin(math.radians(angle)))
            y_speed = int(-speed * math.cos(math.radians(angle)))
        else:
            x_speed = int(speed * math.cos(math.radians(angle)))
            y_speed = int(-speed * math.sin(math.radians(angle)))
    elif direction == 2:
        if magic_number == 1:
            x_speed = int(-speed * math.sin(math.radians(angle)))
            y_speed = int(-speed * math.cos(math.radians(angle)))
        elif magic_number == 4:
            x_speed = int(speed * math.cos(math.radians(angle)))
            y_speed = int(-speed * math.sin(math.radians(angle)))
        elif magic_number == 3:
            x_speed = int(speed * math.sin(math.radians(angle)))
            y_speed = int(speed * math.cos(math.radians(angle)))
        else:
            x_speed = int(-speed * math.cos(math.radians(angle)))
            y_speed = int(speed * math.sin(math.radians(angle)))
    elif direction == 3:
        if magic_number == 1:
            x_speed = int(-speed * math.sin(math.radians(90 - angle)))
            y_speed = int(speed * math.cos(math.radians(90 - angle)))
        elif magic_number == 4:
            x_speed = int(-speed * math.cos(math.radians(90 - angle)))
            y_speed = int(-speed * math.sin(math.radians(90 - angle)))
        elif magic_number == 3:
            x_speed = int(-speed * math.sin(math.radians(90 - angle)))
            y_speed = int(-speed * math.cos(math.radians(90 - angle)))
        else:
            x_speed = int(speed * math.sin(math.radians(90 - angle)))
            y_speed = int(speed * math.cos(math.radians(90 - angle)))
    else:
        if magic_number == 1:
            x_speed = int(speed * math.cos(math.radians(angle)))
            y_speed = int(-speed * math.sin(math.radians(angle)))
        elif magic_number == 4:
            x_speed = int(speed * math.sin(math.radians( angle)))
            y_speed = int(-speed * math.cos(math.radians(angle)))
        elif magic_number == 3:
            x_speed = int(-speed * math.cos(math.radians(angle)))
            y_speed = int(-speed * math.sin(math.radians(angle)))
        else:
            x_speed = int(-speed * math.sin(math.radians(angle)))
            y_speed = int(-speed * math.cos(math.radians(angle)))
    return start_position[0] + x_speed, start_position[1] + y_speed

