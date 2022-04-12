from pycocotools.coco import COCO
import random
import tqdm
import argparse
import shutil
import os



def arg_parser():
    parser = argparse.ArgumentParser('code by rbj')
    parser.add_argument('--annotation_path', type=str,
                        default='data/annotations.json')
    # 生成的txt文件保存的目录
    parser.add_argument('--save_base_path', type=str, default='data/taco/labels/')
    args = parser.parse_args()
    return args


def create_dir(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)


def split_trainset(train_num, total_img):
    random.seed(0)
    train_writer = open('train_set.txt', 'w', encoding='utf-8')
    val_writer = open('val_set.txt', 'w', encoding='utf-8')
    line_num = range(total_img)
    train_index = random.sample(line_num, train_num)

    data_reader = open('dataSetPath.txt', 'r')
    data = data_reader.readlines()
    for i in line_num:
        if i in train_index:
            train_writer.write(data[i])
        else:
            val_writer.write(data[i])
    train_writer.close()
    val_writer.close()
    data_reader.close()


if __name__ == '__main__':
    trainval = 0.9
    total_img = 0
    label_transfer = {5: 0, 7: 1, 12: 2, 29: 3,
                      36: 4, 39: 5, 58: 6, 59: 7}
    class_num = {}

    args = arg_parser()
    annotation_path = args.annotation_path

    data_source = COCO(annotation_file=annotation_path)
    catIds = data_source.getCatIds()
    categories = data_source.loadCats(catIds)
    categories.sort(key=lambda x: x['id'])
    classes = {}
    coco_labels = {}
    coco_labels_inverse = {}
    for c in categories:
        coco_labels[len(classes)] = c['id']
        coco_labels_inverse[c['id']] = len(classes)
        classes[c['name']] = len(classes)

    img_ids = data_source.getImgIds()
    trainSetPath = 'dataSetPath.txt'
    with open(trainSetPath, mode='w') as fp:
        for index, img_id in tqdm.tqdm(enumerate(img_ids), desc='change .json file to .txt file'):
            img_info = data_source.loadImgs(img_id)[0]
            save_name = img_info['file_name'].replace('/', '_')
            # file_name = save_name.split('.')[0]
            height = img_info['height']
            width = img_info['width']

            is_exist = False
            lines = ''
            lines = lines + '%s/'%(os.path.abspath('data/taco/images')) + save_name
            annotation_id = data_source.getAnnIds(img_id) # 获取每张图片的标签 id
            if len(annotation_id) == 0:
                fp.write('')
                continue
            annotations = data_source.loadAnns(annotation_id)

            for annotation in annotations:
                label = coco_labels_inverse[annotation['category_id']]
                if label in label_transfer.keys():
                    is_exist = True
                    box = annotation['bbox']
                    # some annotations have basically no width / height, skip them
                    if box[2] < 1 or box[3] < 1:
                        continue
                    # top_x,top_y,width,height---->x_min,y_min,x_max,y_max
                    b = (int(float(box[0])), int(float(box[1])),
                         int(float(box[0] + box[2])), int(float(box[1] + box[3])))
                    label = label_transfer[label]
                    if label not in class_num.keys():
                        class_num[label] = 0
                    class_num[label] += 1
                    lines = lines + ' ' + ",".join([str(a) for a in b]) + ',' + str(label)

            if is_exist:
                lines = lines + '\n'
                fp.writelines(lines)
                total_img += 1
            else:
                continue


    print(class_num)
    print('finish')
    print('total_img: ', total_img)
    train_num = int(total_img*trainval)
    split_trainset(train_num, total_img)


