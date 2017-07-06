# coding=utf-8
from PIL import Image
import env

def generate_map(random=False):
    """生成地图的矩阵形式，输出三个矩阵，分别是图案矩阵、背景矩阵以及前景矩阵如果random参数为True
       则地图的Shape随机生成，否则从env中的预制背景矩阵中随机挑选一个，基于此生成其他两个矩阵
    """
    # 生成背景
    color_map, bg_map = env.bg_map_gen()
    color_map = env.color_map_gen(color_map, bg_map)
    fg_map = env.fg_map_gen(color_map)

    return color_map, bg_map, fg_map


def map_normalization(color_matrix, bg_matrix, fg_matrix):
    """根据三个矩阵，组合为所有唯一的图案对应的编码，为后续的绘图做准备"""
    return None


def draw_map(normalized_map):
    """根据输入矩阵，随机挑选背景图片，并按照矩阵中的内容计算相应的坐标，将图片粘贴到相应位置"""
    return None


def create_one(random=False):
    c, b, f = generate_map(random=random)
    n = map_normalization(c, b, f)
    return draw_map(n)


def main():
    x, y, z = generate_map()
    print x
    print y
    print z


if __name__ == '__main__':
    main()
