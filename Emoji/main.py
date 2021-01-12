# This is a sample Python script.
import matplotlib.pyplot as plt
from scipy import spatial
from PIL import Image
import numpy as np
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def show_img(name):
    # 设置画布
    plt.figure()
    # 去除坐标轴
    plt.axis('off')
    # 显示图片
    plt.imshow(name)
    # # 保存emoji马赛克风格图像，去除白边
    # plt.savefig('image_emoji.png', bbox_inches="tight", pad_inches=0.0)

    # plt.show()

def test(size):
    im = np.array(Image.open("LBXX.jpg").resize([size, size]).getdata()).reshape([size, size, 3])/256
    # print(np.array(Image.open("LBXX.jpg").resize([50, 50]).getdata())/256)

    #显示图片
    plt.figure()
    plt.imshow(im)
    # plt.title(Original Image)
    plt.show()

    # 读取emoji数据
    emoji_array = np.load("emojis_16.npy")
    print("emoji个数： ", len(emoji_array))
    print(len(emoji_array[0]))
    # print(emoji_array[0])

    # 获取emoji的平均颜色值
    emoji_mean_array = np.array([ar.mean(axis=(0, 1)) for ar in emoji_array])

    # 将得到的每个emoji平均颜色值存储在树中以加快搜索速度
    tree = spatial.KDTree(emoji_mean_array)

    indices= []
    #二维数据转一维
    flattened_img = im.reshape(-1, im.shape[-1])
    print(flattened_img.shape)

    # 匹配最相似的表情符号的像素(最近邻算法:tree.query返回最近数组的下标)
    for pixel in flattened_img:
        pixel_ = np.concatenate((pixel, [1]))
        # 查询最近的索引
        _, index = tree.query(pixel_)
        indices.append(index)

    # print(indices)
    # 从索引中获取对应的表情符号
    emoji_matches = emoji_array[indices]
    # 查看表情
    # for i in range(10):
    #     show_img(emoji_matches[i])
    print("符号个数： ", len(emoji_matches))

    # 获取图片的高度
    dim = im.shape[0]
    print(dim)

    # 设置最终生成图像的大小，每个表情符号的形状都是(16,16,4)，R, G, B, alpha
    resized_ar = emoji_matches.reshape((dim, dim, 16, 16, 4))

    # 转换单个表情符号补丁（5维）
    # 使用numpy块生成完整的图像(三维)
    final_img = np.block([[[x] for x in row] for row in resized_ar])

    # 设置画布
    plt.figure()
    # 去除坐标轴
    plt.axis('off')
    # 显示图片
    plt.imshow(final_img)
    # 保存emoji马赛克风格图像，去除白边
    plt.savefig('image_emoji.png', bbox_inches="tight", pad_inches=0.0)

    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    test(20)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
