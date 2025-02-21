from classes.ImageEnum import ImageSource
import cv2
from PyQt5.QtGui import QPixmap , QImage

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

    def apply_uniform_noise(self):
        if(self.input_image_1.input_image is not None):
            self.input_image_1.apply_noise('uniform')
        if(self.input_image_2.input_image is not None ):
            self.input_image_2.apply_noise('uniform')
        self.set_output_image_source()
        
    def apply_salt_and_pepper_noise(self):
        if(self.input_image_1.input_image is not None):
            self.input_image_1.apply_noise('salt_pepper')
        if(self.input_image_2.input_image is not None ):
            self.input_image_2.apply_noise('salt_pepper')
        self.set_output_image_source()
        
    def reset_output_image_to_normal(self):
        self.input_image_1.output_image = self.input_image_1.input_image
        self.input_image_2.output_image = self.input_image_2.input_image
        self.set_output_image_source()

    
    def numpy_to_qpixmap(self, image_array):
        """Convert NumPy array to QPixmap"""
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        height, width, channels = image_array.shape
        bytes_per_line = channels * width
        qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)