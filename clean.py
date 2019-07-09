import sys
import re

regex = re.compile('[^a-zA-Z*]')

class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def read_file(path):
    with open(path, 'r') as f:
        file_data = f.readlines()
    return [l.strip() for l in file_data if l.strip()]


field = []
mine_count = 0
for data in read_file(sys.argv[1]):
  mine_count += len(regex.sub('', data))
  field.append([char for char in data])

script = read_file(sys.argv[2])

DIRECTION = DotDict({
    'UP': 0,
    'DOWN': 1,
    'LEFT': 2,
    'RIGHT': 3
})


def get_field_dimension():
    return [len(field), len(field[0])]


matrix = get_field_dimension()


def get_new_center():
    return [int((matrix[0] - 1) / 2), int((matrix[1] - 1) / 2)]


center_coords = get_new_center()


def add_column(direction):
    for i, r in enumerate(field):
        if direction == DIRECTION.LEFT:
            r.insert(0, ".")
        elif direction == DIRECTION.RIGHT:
            r.append(".")
        field[i] = r


def add_row(direction):
    if direction == DIRECTION.UP:
        field.insert(0, ["."] * len(field[0]))
    elif direction == DIRECTION.DOWN:
        field.append(["."] * len(field[0]))


def remove_column(direction):
    for i, r in enumerate(field):
        if direction == DIRECTION.LEFT:
            r.pop(0)
        elif direction == DIRECTION.RIGHT:
            r.pop(len(r) - 1)
        field[i] = r


def remove_row(direction):
    if direction == DIRECTION.UP:
        del field[0]
    elif direction == DIRECTION.DOWN:
        del field[len(field) - 1]


def check_for_empty_space(direction, limit):
    remove = True
    if direction == DIRECTION.LEFT:
        for i in range(0, limit):
            col = [field[j][i] for j in range(matrix[0])]
            if "".join(col) != "." * matrix[0]:
                remove = False
                break
    elif direction == DIRECTION.RIGHT:
        for i in range(0, limit):
            col = [field[j][(matrix[1] - 1 - i)] for j in range(matrix[0])]
            if "".join(col) != "." * matrix[0]:
                remove = False
                break
    elif direction == DIRECTION.UP:
        for i in range(0, limit):
            if "".join(field[i]) != "." * matrix[1]:
                remove = False
                break
    elif direction == DIRECTION.DOWN:
        for i in range(0, limit):
            if "".join(field[matrix[0] - 1 - i]) != "." * matrix[1]:
                remove = False
                break
    return remove


def make_vessel_to_center(remove_dir, add_dir, req_space):

    if check_for_empty_space(remove_dir, req_space):
        for _ in range(req_space):
            if remove_dir in [DIRECTION.UP, DIRECTION.DOWN]:
                remove_row(remove_dir)
            else:
                remove_column(remove_dir)
    else:
        for _ in range(req_space):
            if add_dir in [DIRECTION.UP, DIRECTION.DOWN]:
                add_row(add_dir)
            else:
                add_column(add_dir)


def fall_vessel_1km():
    for i, r in enumerate(field):
        for j, c in enumerate(r):
            if c != "." and c != "*":
                if c == "a":
                    r[j] = "*"
                else:
                    r[j] = chr(ord(c) - 1)
        field[i] = r


def is_mine_visible():
    mine_visible = False
    for i, r in enumerate(field):
        for j, c in enumerate(r):
            if c != ".":
                mine_visible = True
                break
    return mine_visible


def is_mine_missed():
    missed = True
    for i, r in enumerate(field):
        for j, c in enumerate(r):
            if c != "." and c != "*":
                missed = False
                break
    return missed


for row in field:
    print("".join(row))

command_count = 1
dir_count = 0
fire_count = 0


for command in script:
    if is_mine_missed():
        break
    print("Step {}".format(command_count))
    actions = command.split(" ")
    print("\n")
    print(command)
    print("\n")

    for action in actions:
        if action == "north":
            # increment y coordinate of ship
            current_x = center_coords[0] - 1
            down = matrix[0] - 1 - current_x
            up = matrix[0] - 1 - down
            r_space = down - up
            make_vessel_to_center(DIRECTION.DOWN, DIRECTION.UP, r_space)
            dir_count += 1

        if action == "south":
            # decrement y-coordinate of ship
            current_x = center_coords[0] + 1
            down = matrix[0] - 1 - current_x
            up = matrix[0] - 1 - down
            r_space = up - down
            make_vessel_to_center(DIRECTION.UP, DIRECTION.DOWN, r_space)
            dir_count += 1

        if action == "east":
            # increment x-coordinate of ship
            current_y = center_coords[1] + 1
            right = matrix[1] - 1 - current_y
            left = matrix[1] - 1 - right
            r_space = left - right
            make_vessel_to_center(DIRECTION.LEFT, DIRECTION.RIGHT, r_space)
            dir_count += 1

        if action == "west":
            # decrement x-coordinate of ship
            current_y = center_coords[1] - 1
            right = matrix[1] - 1 - current_y
            left = matrix[1] - 1 - right
            r_space = right - left
            make_vessel_to_center(DIRECTION.RIGHT, DIRECTION.LEFT, r_space)
            dir_count += 1
        try:
            if action == "alpha":
                fire_count += 1
                field[center_coords[0] - 1][center_coords[1] - 1] = "."
                field[center_coords[0] - 1][center_coords[1] + 1] = "."
                field[center_coords[0] + 1][center_coords[1] - 1] = "."
                field[center_coords[0] + 1][center_coords[1] + 1] = "."

            if action == "beta":
                fire_count += 1
                field[center_coords[0] - 1][center_coords[1]] = "."
                field[center_coords[0]][center_coords[1] - 1] = "."
                field[center_coords[0]][center_coords[1] + 1] = "."
                field[center_coords[0] + 1][center_coords[1]] = "."

            if action == "gamma":
                fire_count += 1
                field[center_coords[0]][center_coords[1] - 1] = "."
                field[center_coords[0]][center_coords[1]] = "."
                field[center_coords[0]][center_coords[1] + 1] = "."

            if action == "delta":
                fire_count += 1
                field[center_coords[0] + 1][center_coords[1]] = "."
                field[center_coords[0]][center_coords[1]] = "."
                field[center_coords[0] - 1][center_coords[1]] = "."
        except IndexError as e:
            pass

    matrix = get_field_dimension()
    center_coords = get_new_center()

    fall_vessel_1km()

    if not is_mine_visible():
        print(".")
    else:
        for row in field:
            print("".join(row))

    command_count+=1

def calculate_score(mine_count, dir_count, fire_count):
    mine_count_ = 10*mine_count
    fire_count = [5*fire_count if 5*fire_count < 5*mine_count else 5*mine_count]
    dir_count = [2*dir_count if 2*dir_count < 3*mine_count else 3*mine_count]
    return mine_count_-fire_count[0]-dir_count[0]

def check_status_score():
    final_mine_count = 0
    status = "fail"
    score = 0
    for field_ in field:
        for line in field_:
            final_mine_count += len(regex.sub('', line))

    if (command_count == len(script)+1) and (final_mine_count == 0):
        status = "pass"
        score = calculate_score(mine_count, dir_count, fire_count)
    elif (command_count != len(script)+1) and (final_mine_count == 0):
        status = "pass"
        score = 1
    return status, score

status, score = check_status_score()

print("{} ({})".format(status, score))