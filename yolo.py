import cv2
import os
import numpy as np
from aruco import *

yolo_folder = 'yolov3/'
yolo_weights_seeds = yolo_folder + 'yolov3_custom_one_class_last_seeds.weights'
yolo_weights_sunflowers = yolo_folder + 'yolov3_custom_one_class_last_sunflowers.weights'
yolo_cfg     = yolo_folder + 'yolov3_custom_one_class.cfg'
yolo_classes = yolo_folder + 'classes.txt'

net_seeds = cv2.dnn.readNet(yolo_weights_seeds, yolo_cfg)
net_sunflowers = cv2.dnn.readNet(yolo_weights_sunflowers, yolo_cfg)

with open (yolo_classes) as f:
    labels = f.read().strip().split('\n')
layer_names = net_seeds.getLayerNames()
out_layer_indexes = [index[0] - 1 for index in net.getUnconnectedOutLayers()]
out_layer_names = [layer_names[index] for index in out_layer_indexes]

def find_seeds(img):
    height, width, _ = img.shape
    size = (608, 608)
    
    blob = cv2.dnn.blobFromImage(img, 1/255,  size, swapRB=True)
    net_seeds.setInput(blob)
    out_layers = net_seeds.forward(out_layer_names)
    
    object_boxes = []
    object_probas = []
    object_labels = []
    
    for layer in out_layers:
        for result in layer:
            x, y, w, h = result[:4]
            x = int(x * width)
            y = int(y * height)
            w = int(w * width)
            h = int(h * height)
            
            #Находим наиболее вероятный класс объекта
            probas = result[5:]
            max_proba_index = np.argmax(probas)
            max_proba = probas[max_proba_index]
            
            #Если есть вероятность, что это какой-то объект
            if max_proba > 0:
                #Записываем информацию о нем в массивы с данными
                object_boxes.append([x, y, w, h])
                object_probas.append(float(max_proba))
                object_labels.append(labels[max_proba_index])
                
    #Применяем NMS-преобразование, чтобы объединить рамки одного и того же объкта
    filtered_boxes = cv2.dnn.NMSBoxes(object_boxes, object_probas, 0.0, 0.2)
    
    #Запишем все данные о наших объектах в массив
    objects = []
    for index_arr in filtered_boxes:
        index = index_arr[0]
        x, y, w, h = object_boxes[index]
        label = object_labels[index]
        proba = object_probas[index]
        objects.append((label, (x, y, w, h), proba))
        
    return objects

def find_sunflowers(img):
    height, width, _ = img.shape
    size = (608, 608)
    
    blob = cv2.dnn.blobFromImage(img, 1/255,  size, swapRB=True)
    net_sunflowers.setInput(blob)
    out_layers = net_sunflowers.forward(out_layer_names)
    
    object_boxes = []
    object_probas = []
    object_labels = []
    
    for layer in out_layers:
        for result in layer:
            x, y, w, h = result[:4]
            x = int(x * width)
            y = int(y * height)
            w = int(w * width)
            h = int(h * height)
            
            #Находим наиболее вероятный класс объекта
            probas = result[5:]
            max_proba_index = np.argmax(probas)
            max_proba = probas[max_proba_index]
            
            #Если есть вероятность, что это какой-то объект
            if max_proba > 0:
                #Записываем информацию о нем в массивы с данными
                object_boxes.append([x, y, w, h])
                object_probas.append(float(max_proba))
                object_labels.append(labels[max_proba_index])
                
    #Применяем NMS-преобразование, чтобы объединить рамки одного и того же объкта
    filtered_boxes = cv2.dnn.NMSBoxes(object_boxes, object_probas, 0.0, 0.2)
    
    #Запишем все данные о наших объектах в массив
    objects = []
    for index_arr in filtered_boxes:
        index = index_arr[0]
        x, y, w, h = object_boxes[index]
        label = object_labels[index]
        proba = object_probas[index]
        objects.append((label, (x, y, w, h), proba))
        
    return objects

def count_seeds(filename):
	img = cv2.imread(filename)
	seeds = find_seeds(img)
	return len(seeds)

def get_sunflower_size(filename, dist):
	img = cv2.imread(filename)
	sunflowers = find_sunflowers(img)
	sunflower_size_px = max(sunflowers[1])
	marker_size_px = markerDistance(img)
	return sunflower_size_px/marker_size_px*dist

	