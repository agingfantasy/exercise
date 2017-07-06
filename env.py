# coding=utf-8
import numpy as np


"""
    State:      |   Background   |   Foreground 
    0: Empty    |   0: Forbidden |   0: Normal
    ----------  |   1: Normal    |   1: Chained
    1: Blue     |   2: Yellow
    2: Red      |   3: White
    3: Green
    4: Gold
    5: White
    ----------
    6: Bomb1
    7: Bomb2
    8: Bomb3
    9: Bomb4
    ----------
    10: Loess
    11: Gold
    ----------
    12: Flash
"""

ColorState = [1, 2, 3, 4, 5]
BombState = [6, 7, 8, 9]

"""固定地图部分
"""

# 1. 第一关地图背景 7 X 7
NO_01_BGMAP = np.array([
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 1, 1, 1],
    [1, 1, 2, 2, 1, 1, 1],
    [1, 1, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
], dtype=np.int8)

# 2. 第二关地图背景 8 X 10
NO_02_BGMAP = np.array([
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 2, 2, 1, 1, 1, 1, 0],
    [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 2, 2, 2, 1, 1],
    [0, 1, 1, 1, 1, 2, 2, 2, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
], dtype=np.int8)

# 3. 第三关地图背景 12 X 9
NO_03_BGMAP = np.array([
    [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
    [0, 0, 1, 1, 2, 2, 2, 2, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 2, 2, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
], dtype=np.int8)

# 4. 第四关地图背景 11 X 9
NO_04_BGMAP = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
], dtype=np.int8)

# 5. 第五关地图背景 9 X 9
NO_05_BGMAP = np.array([
    [1, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 1],
], dtype=np.int8)


def bg_map_gen(random=False):
    if random:
        row = np.random.randint(7, 12)
        col = np.random.randint(row - 2, min(row + 2, 12))
        return bg_map_internal(row, col)
    else:
        preconfig_fg = [NO_01_BGMAP, NO_02_BGMAP, NO_03_BGMAP, NO_04_BGMAP, NO_05_BGMAP]
        bg_map = preconfig_fg[np.random.randint(0, len(preconfig_fg)-1)]
        return bg_map_internal(bg_map.shape[0], bg_map.shape[1], bg_map)


def bg_map_internal(row, col, template=None):
    color_map = np.zeros((row, col), np.int8)
    if template is not None:
        bg_map = template
    else:
        bg_map = np.ones((row, col), np.int8)
    bg_prob = normalize(np.random.choice(100, 5))

    # 以下部分copy自menghuanEnv中的fill_random_background
    count = int(row * col * (bg_prob[4] + bg_prob[5]))
    if count > 0:
        l_max = min(count, col)
        l_min = max(count // row + 1, 1)
        l = np.random.randint(l_min, l_max + 1)
        h = max(count // l, 1)
        s0 = np.random.randint(row - h + 1)
        s1 = np.random.randint(col - l + 1)
        for r in range(s0, s0 + h):
            for c in range(s1, s1 + l):
                bg_map[(r, c)] = 1
                if np.random.rand() < bg_prob[4] / (bg_prob[4] + bg_prob[5]):
                    color_map[(r, c)] = 10
                else:
                    color_map[(r, c)] = 11
    if template is not None:
        return color_map, bg_map

    for r in range(row):
        for c in range(col):
            if color_map[(r, c)] in [10, 11]:
                bg_map[(r, c)] = 1
                continue
            k = (np.cumsum(bg_prob) > np.random.rand()).argmax()
            if k == 0:
                if c == 1 or c == col - 1:
                    count = 1
                else:
                    count = 2
                off = c - 1
                while count > 0 and bg_map[(r, off)] == 0:
                    count -= 1
                if count == 0:
                    k = 1
            elif k in (4, 5):
                continue
            bg_map[(r, c)] = k

    return color_map, bg_map


def normalize(prob_list):
    result = []
    new_prob_list = prob_list.tolist()
    non_color_rate = 1.0 - float(np.random.randint(50, 75))/100
    total = sum(prob_list) / non_color_rate
    new_prob_list.insert(1, int(total * (1.0 - non_color_rate)))
    for x in new_prob_list:
        result.append(float(x)/total)
    return result


def color_map_gen(color_map, bg_map):
    m = color_map
    for r in range(color_map.shape[0]):
        for c in range(color_map.shape[1]):
            if bg_map[(r, c)] in (1, 2, 3) and color_map[(r, c)] == 0:
                m[(r, c)] = np.random.randint(1, len(ColorState) + 1)
                while r > 1 and m[(r-2, c)] == m[(r-1, c)] == m[(r, c)] or \
                    c > 1 and m[(r, c-2)] == m[(r, c-1)] and m[(r, c-1)] == m[(r, c)]:
                    m[(r, c)] = np.random.randint(1, len(ColorState) + 1)
    return m


def fg_map_gen(color_map):
    chain_rate1 = 0.5
    chain_rate2 = 0.1
    fg_map = np.zeros((color_map.shape[0], color_map.shape[1]), np.int8)
    if np.random.rand() < chain_rate1:
        for r in range(color_map.shape[0]):
            for c in range(color_map.shape[1]):
                if color_map[(r, c)] in [1, 2, 3, 4, 5] and np.random.rand() < chain_rate2:
                    fg_map[(r, c)] = 1
    return fg_map

