from classes.ImageEnum import ImageSource
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap , QImage
from copy import deepcopy
class Controller():
    def __init__(self , input_image_1 , input_image_2 , output_image , output_image_label):
        self.input_image_1 = input_image_1
        self.input_image_2 = input_image_2
        self.output_image = output_image
        self.current_output_source_index = 0
        self.output_image_label = output_image_label

    def set_output_image_source(self):
        if(self.current_output_source_index == 1):
            self.output_image_pixmap = self.numpy_to_qpixmap(self.input_image_1.output_image)
        elif(self.current_output_source_index == 2):
            self.output_image_pixmap = self.numpy_to_qpixmap(self.input_image_2.output_image)
                
        self.output_image_label.setPixmap(self.output_image_pixmap)
        self.output_image_label.setScaledContents(True)
    
    def browse_image_input_1(self):
        self.input_image_1.select_image()
    
    def browse_image_input_2(self):
        self.input_image_2.select_image()

    def apply_noise(self , noise_type, mean = 0, std = np.sqrt(0.1)):
        if(self.input_image_1.input_image is not None):
            self.input_image_1.apply_noise(noise_type, mean ,std)
        if(self.input_image_2.input_image is not None ):
            self.input_image_2.apply_noise(noise_type , mean , std)
        self.set_output_image_source()
        
        
    def reset_output_image_to_normal(self):
        self.input_image_1.output_image = deepcopy(self.input_image_1.input_image)
        self.input_image_2.output_image = deepcopy(self.input_image_2.input_image)
        self.set_output_image_source()

    def rgb2grey(self):
        if(self.input_image_1.input_image is not None):
            self.input_image_1.output_image = self.input_image_1.convert_rgb_to_gray(self.input_image_1.input_image)
        if(self.input_image_2.input_image is not None ):
            self.input_image_2.output_image = self.input_image_2.convert_rgb_to_gray(self.input_image_2.input_image)
        self.set_output_image_source()
    
    def apply_time_domain_low_pass(self , filter_type):
        if(self.input_image_1.input_image is not None):
            self.input_image_1.apply_filter(filter_type)
        if(self.input_image_2.input_image is not None ):
            self.input_image_2.apply_filter(filter_type)
        self.set_output_image_source()

    
    def numpy_to_qpixmap(self, image_array):
        """Convert NumPy array to QPixmap"""
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        height, width, channels = image_array.shape
        bytes_per_line = channels * width
        qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)