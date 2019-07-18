#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def save_xml(image_name, bbox, class_dict, save_dir='./VOC2007/Annotations', width=1920, height=1080, channel=3):
    '''
    将CSV中的一行
    000000001.jpg [[1,2,3,4],...]
    转化成
    000000001.xml

    :param image_name:图片名
    :param bbox:对应的bbox
    :param save_dir:
    :param width:这个是图片的宽度，博主使用的数据集是固定的大小的，所以设置默认
    :param height:这个是图片的高度，博主使用的数据集是固定的大小的，所以设置默认
    :param channel:这个是图片的通道，博主使用的数据集是固定的大小的，所以设置默认
    :return:
    '''
    from lxml.etree import Element, SubElement, tostring
    from xml.dom.minidom import parseString

    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'JPEGImages'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '%s' % channel

    for x, y, w, h, c in bbox:
        left, top, right, bottom = x, y, x + w, y + h
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = class_dict[c]
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = '%s' % left
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = '%s' % top
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = '%s' % right
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = '%s' % bottom

    xml = tostring(node_root, pretty_print=True)  
    dom = parseString(xml)

    save_xml = os.path.join(save_dir, image_name.replace('jpg', 'xml'))
    with open(save_xml, 'wb') as f:
        f.write(xml)

    return

def txt2xml( txt_name, save_path ):
    class_dict = ['background', 'car', 'trunck']
    
    boxes = []
    img_name = os.path.basename(txt_name )
    
    with open( txt_name, 'r') as f:
        for line in f:
            temp = line.strip().split(" ")
            if len(temp) > 1:        
                boxes.append([temp[0], float(temp[1])*w, float(temp[2])*h, float(temp[3])*w, float(temp[4])*h])
                save_xml(img_name, boxes, class_dict, save_path )
                
                
def change2xml(label_dict={}):
    for image in label_dict.keys():
        image_name = os.path.split(image)[-1]
        bbox = label_dict.get(image, [])
        save_xml(image_name, bbox)
    return


if __name__ == '__main__':
    # step 2
    # make_voc_dir()

    # step 3
    # label_dict = utils.read_csv(csv_path=r'./train_b.csv',
    #                             pre_dir=r'/home/matthew/dataset')
    # rename_image(label_dict)

    # step 3
    label_dict = utils.read_csv(csv_path=r'./rename_train_b.csv',
                                pre_dir=r'/home/matthew/VOC2007/JPEGImages')
    change2xml(label_dict)