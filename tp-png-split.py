

import plistlib
import os
import os.path
import sys
from PIL import Image


def export_image(img, pathname, item):
    # 去透明后的子图矩形
    x, y, w, h = tuple(map(int, item['textureRect']))
    # 子图原始大小
    size = tuple(map(int, item['spriteSourceSize']))
    # 子图在原始图片中的偏移
    if(item['spriteOffset'][0].find('.') > 0 or item['spriteOffset'][1].find('.') > 0):
        print(">>>>>>>>>>>not save>>>>>>>>>>>>")
        print(pathname, item['spriteOffset'][0],item['spriteOffset'][1])
        print("<<<<<<<<<<<<<<<not sav<<<<<<<<<<<")
        return
    ox, oy = tuple(map(int, item['spriteOffset']))


    

    # 获取子图左上角，右下角
    if item['textureRotated']:
        box = (x, y, x + h, y + w)
    else:
        box = (x, y, x + w, y + h)

    # 使用原始大小创建图像，全透明
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    # 从图集中裁剪出子图
    sprite = img.crop(box)

    # rotated纹理旋转90度
    if item['textureRotated']:
        sprite = sprite.transpose(Image.ROTATE_90)

    # 粘贴子图，设置偏移
    image.paste(sprite, (ox, oy))

    # 保存到文件
    print('保存文件：%s' % pathname)

    pathdir = os.path.split(pathname)[0]
    if(not os.path.exists(pathdir)):
        os.makedirs(pathdir)

    image.save(pathname, 'png')

# 获取 frame 参数
def get_frame(frame):
    result = {}
    if 'textureRect' in frame:

        result['textureRect'] = frame['textureRect'].replace('}', '').replace('{', '').split(',')
        result['spriteSourceSize'] = frame['spriteSourceSize'].replace('}', '').replace('{', '').split(',')
        result['spriteOffset'] = frame['spriteOffset'].replace('}', '').replace('{', '').split(',')
        result['textureRotated'] = frame['textureRotated']
    if 'frame' in frame:
        result['textureRect'] = frame['frame'].replace('}', '').replace('{', '').split(',')
        result['spriteSourceSize'] = frame['sourceSize'].replace('}', '').replace('{', '').split(',')
        result['spriteOffset'] = frame['offset'].replace('}', '').replace('{', '').split(',')
        result['textureRotated'] = frame['rotated']
    return result

# 生成图片
def gen_image(file_name, export_path):
    # 检查文件是否存在
    plist = file_name + '.plist'
    if not os.path.exists(plist):
        print('plist文件【%s】不存在！请检查' % plist)
        return

    png = file_name + '.png'
    if not os.path.exists(png):
        print('png文件【%s】不存在！请检查' % plist)
        return

    # 检查导出目录
    if not os.path.exists(export_path):
        try:
            os.mkdir(export_path)
        except Exception as e:
            print(e)
            return

    # 使用plistlib库加载 plist 文件
    lp = plistlib.load(open(plist, 'rb'))
    # 加载 png 图片文件
    img = Image.open(file_name + '.png')

    # 读取所有小图数据
    if not 'frames' in lp:
        print(">>>>>>>>>>>>>>>>>>>>>>>")
        print(file_name)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<")
        return

    frames = lp['frames']
    # print(frames)
    for key in frames:
        # print(key)
        # print(frames[key])
        item = get_frame(frames[key])
        export_image(img, os.path.join(export_path, key), item)


# gen_image("fireball_sub_explosion", "fireball_sub_explosion")


# 遍历文件夹
def walkFile(file):
    print("---------------")
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            imgPath = os.path.join(root, f)
            if f.endswith('.plist'):
                imgPath = os.path.join(root, f)
                file_name = os.path.splitext(imgPath)[0]
                gen_image(file_name,file_name)

                

            
walkFile(".")
