import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import inception_v3
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

import numpy as np
import cv2
class prediction_disease_type:
    def __init__(self,img,plant):
        self.img = img
        self.plant = plant
        self.label_disease = {
            0 : 'Apple___Apple_scab',
            1 : 'Apple___Black_rot',
            2 : 'Apple___Cedar_apple_rust',
            3 : 'Apple___healthy',
            4 : 'Background_without_leaves',
            5 : 'Blueberry___healthy',
            6 : 'Cherry___Powdery_mildew',
            7 : 'Cherry___healthy',
            8 : 'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
            9 : 'Corn___Common_rust',
            10: 'Corn___Northern_Leaf_Blight',
            11: 'Corn___healthy',
            12: 'Grape___Black_rot',
            13: 'Grape___Esca_(Black_Measles)',
            14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            15: 'Grape___healthy',
            16: 'Orange___Haunglongbing_Citrus_greening',
            17: 'Peach___Bacterial_spot',
            18: 'Peach___healthy',
            19: 'Pepper_bell___Bacterial_spot',
            20: 'Pepper_bell___healthy',
            21: 'Potato___Early_blight',
            22: 'Potato___Late_blight',
            23: 'Potato___healthy',
            24: 'Raspberry___healthy',
            25: 'Soybean___healthy',
            26: 'Squash___Powdery_mildew',
            27: 'Strawberry___Leaf_scorch',
            28: 'Strawberry___healthy',
            29: 'Tomato___Bacterial_spot',
            30: 'Tomato___Early_blight',
            31: 'Tomato___Late_blight',
            32: 'Tomato___Leaf_Mold',
            33: 'Tomato___Septoria_leaf_spot',
            34: 'Tomato___Spider_mites_Two-,spotted_spider_mite',
            35: 'Tomato___Target_Spot',
            36: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            37: 'Tomato___Tomato_mosaic_virus',
            38: 'Tomato___healthy',
        }
        self.plant_label_disease={
            "Apple":[0,1,2,3],
            "Background_without_leaves":[4],
            "Blueberry" : [5],
            "Cherry" : [6,7],
            "Corn" : [8,9,10,11],
            "Grape" : [12,13,14,15],
            "Orange" : [16] ,
            "Peach" : [17,18],
            "Pepper" : [19,20],
            "Potato" : [21,22,23],
            "Raspberry" : [24],
            "Soybean" : [25],
            "Squash" : [26],
            "Strawberry" : [27,28],
            "Tomato" : [29,30,31,32,33,34,35,36,37,38]
        }
        HEIGHT = 100
        WIDTH = 100
        num_classes =39
        dnn_model = Sequential()

        imported_model = inception_v3.InceptionV3(
                            include_top=False,
                            input_shape=(HEIGHT,WIDTH,3),
                            pooling='avg', 
                            classes=num_classes)
        for layer in imported_model.layers:
                layer.trainable = True

        dnn_model.add(imported_model)
        dnn_model.add(Flatten())
        dnn_model.add(Dense(256, activation='relu'))
        dnn_model.add(Dense(num_classes, activation='softmax'))
        # dnn_model.summary()
        dnn_model.compile(optimizer=Adam(learning_rate=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
        with open('C:/Users/hp/Downloads/model_weightsInceptionACC96.pkl', 'rb') as file:
            loaded_weights = pickle.load(file)
        self.dnn_model = dnn_model
        # Set the loaded weights to the model
        dnn_model.set_weights(loaded_weights)
        self.dnn_model = dnn_model
        print("done")
    def get_label(self):
        process_img = cv2.resize(self.img, (100, 100),interpolation = cv2.INTER_LINEAR)
        process_img = process_img/(255)
        process_img = np.expand_dims(process_img, axis=0)
        y_pred = self.dnn_model.predict(process_img)
        
        indx = np.argmax(y_pred)
        disease_pred = self.label_disease[indx]
        max_prob_indx = self.plant_label_disease[self.plant][0]
        for x in self.plant_label_disease[self.plant]:
            print(x,y_pred[0][x],max_prob_indx,y_pred[0][max_prob_indx])
            if y_pred[0][x]>y_pred[0][max_prob_indx]:
                max_prob_indx = x
        return [(y_pred[0][max_prob_indx],self.label_disease[max_prob_indx]),(y_pred[0][indx],self.label_disease[indx])]
     
if __name__ == "__main__":
      
    pass
        
