#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:45:05 2021
@author: Priyabrata Sahoo
"""
import numpy as np
import torch
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from countwheatgrains import count


class ricegrains:
    def __init__(self, filename):
        self.filename = filename

    # This functions helps to upload the image on the ui front and helps to convert the image to required format so that the image could be predicted
    def predictionricegrains(self):
        # load model
        model = load_model('/home/knoldus/Downloads/ricegrains50epoc(1).h5', compile=False)

        # imagename = '/home/knoldus/Downloads/objectdetectionwheat/yolov5/static/inputImage.jpg'
        imagename= self.filename
        test_image = image.load_img(imagename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict_proba(test_image)
        # print(result)
        finalresult = {}

        finalresult['Broken'] = result[0][0]
        finalresult['Damaged'] = result[0][1]
        finalresult['ForeignMatters'] = result[0][2]
        finalresult['Healthy'] = result[0][3]
        finalresult['Immature'] = result[0][4]
        finalresult['Potiya'] = result[0][5]
        finalresult['Shrivled'] = result[0][6]
        finalresult['Weevilled'] = result[0][7]
        maxacc=result[0][0]
        import operator
        Prediction= max(finalresult.items(), key=operator.itemgetter(1))[0]
        # for k,v in finalresult.items():
        #     if maxacc <=v:
        #         Prediction=k
        return [{"image": Prediction}, count(), result,finalresult]

        #
        # classes = ['good rice grains', 'bad rice grains']
        # label_name = {classes[i]: result[i] for i in range(len(result))}

        # if result is having value greater that .8 then it will predict good rice grains or else it will predict bad rice
        # grains
        # if result[0][0] >= 0.4:
        #     Prediction = 'Broken'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][1] >= 0.4:
        #     Prediction = 'Damaged'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][2] >= 0.4:
        #     Prediction = 'ForeignMatters'
        #     return [{"image": 'xyz'}, count(), result]
        # elif result[0][3] >= 0.4:
        #     Prediction = 'Healthy'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][4] >= 0.4:
        #     Prediction = 'Immature'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][5] >= 0.4:
        #     Prediction = 'Potiya'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][6] >= 0.4:
        #     Prediction = 'Shrivled'
        #     return [{"image": Prediction}, count(), result]
        # elif result[0][7] >= 0.4:
        #     Prediction = 'Weevilled'
        #     return [{"image": Prediction}, count(), result]
        #
        # return [{"image": 'Probability score is less than threshold'}, count(), result]

