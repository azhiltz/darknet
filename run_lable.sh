#!/bin/bash

./darknet detector test cfg/coco.data cfg/yolov2-tiny.cfg data/yolov2-tiny.weights data/img_list.txt data data/
