from PIL import Image
from PIL import ImageDraw


if __name__ == '__main__':
    f = open('train_set.txt', 'r', encoding='utf-8')
    line = f.readline()
    line = f.readline()
    line = f.readline()
    line = line.split(' ')
    bbox = line[1].split(',')
    x_min = int(bbox[0])
    y_min = int(bbox[1])
    x_max = int(bbox[2])
    y_max = int(bbox[3])
    label = int(bbox[4])

    img = Image.open(line[0])
    a = ImageDraw.ImageDraw(img)
    a.rectangle(((x_min, y_min), (x_max, y_max)), fill=None, outline='red', width=5)
    img.save("text_bbox.jpg")