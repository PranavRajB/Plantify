import cv2
import matplotlib.pyplot as plt
import  numpy as np
from predict_disease import prediction_disease_type
img = cv2.imread("peach_bacteria.jfif")

disease_class = prediction_disease_type(img,"Peach")
print(disease_class.get_label())