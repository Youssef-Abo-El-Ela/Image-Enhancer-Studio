import sys
from PyQt5.QtWidgets import QApplication, QMainWindow , QPushButton , QFrame , QLabel , QVBoxLayout , QCheckBox , QComboBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from classes.image import Image
from classes.controller import Controller
from classes.ImageEnum import ImageSource

compile_qrc()
from icons_setup.icons import *

from icons_setup.compiledIcons import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Image Studio')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))

        # Input Images Initializing
        self.input_image_1 = Image()
        self.input_image_2 = Image()
        
        self.input_image_1_frame = self.findChild(QFrame , "input01Frame")
        self.input_image_1_label = QLabel(self.input_image_1_frame)
        input_image_1_layout = QVBoxLayout(self.input_image_1_frame)
        input_image_1_layout.addWidget(self.input_image_1_label)
        self.input_image_1_frame.setLayout(input_image_1_layout)
        
        self.input_image_2_frame = self.findChild(QFrame , "input02Frame")
        self.input_image_2_label = QLabel(self.input_image_2_frame)
        input_image_2_layout = QVBoxLayout(self.input_image_2_frame)
        input_image_2_layout.addWidget(self.input_image_2_label)
        self.input_image_2_frame.setLayout(input_image_2_layout)
        
        # Adding Noise Checkboxes
        self.apply_noise_checkbox = self.findChild(QCheckBox , "applyNoiseCheckbox")
        self.uniform_noise_checkbox = self.findChild(QCheckBox , "uniformNoiseCheckbox")
        self.salt_noise_checkbox = self.findChild(QCheckBox , "saltNoiseCheckbox")
        self.gaussian_noise_checkbox = self.findChild(QCheckBox , "gaussianNoiseCheckbox")
        
        self.uniform_noise_checkbox.setDisabled(True)
        self.salt_noise_checkbox.setDisabled(True)
        self.gaussian_noise_checkbox.setDisabled(True)
        
        self.apply_noise_checkbox.stateChanged.connect(self.toggle_noise_checkboxes)
        self.uniform_noise_checkbox.stateChanged.connect(self.apply_uniform_noise)
        self.salt_noise_checkbox.stateChanged.connect(self.apply_salt_and_pepper_noise)
        
        
        # Initializing Browse Input Images
        self.browse_image_input_1_button = self.findChild(QPushButton , "pushButton_2") 
        self.browse_image_input_1_button.clicked.connect(self.browse_image_input_1)
        
        self.browse_image_input_2_button = self.findChild(QPushButton , "pushButton_3") 
        self.browse_image_input_2_button.clicked.connect(self.browse_image_input_2)
    
        # Initialize Output Image
        self.output_image = Image()
        self.output_image_frame = self.findChild(QFrame , "outputFrame")
        self.output_image_label = QLabel(self.output_image_frame)
        output_image_frame = QVBoxLayout(self.output_image_frame)
        output_image_frame.addWidget(self.output_image_label)
        self.output_image_frame.setLayout(output_image_frame)
    
        # Selecting Output Image Source
        self.output_image_selector_combobox = self.findChild(QComboBox , "comboBox")
        self.output_image_selector_combobox.currentIndexChanged.connect(self.set_output_image_source)
        
        #Initializing reset button
        self.reset_button = self.findChild(QPushButton , "reset")
        self.reset_button.clicked.connect(self.reset_output_to_input_state)
        
        # Initializing Controller
        self.controller = Controller(self.input_image_1 , self.input_image_2 , self.output_image , self.output_image_label)
        
        
    def browse_image_input_1(self):
        self.controller.browse_image_input_1()
        if (len(self.input_image_1.input_image)):
            self.input_image_1_pixmap = self.controller.numpy_to_qpixmap(self.input_image_1.input_image)
            self.input_image_1_label.setPixmap(self.input_image_1_pixmap)
            self.input_image_1_label.setScaledContents(True)
    
    def browse_image_input_2(self):
        self.controller.browse_image_input_2()
        if (len(self.input_image_2.input_image)):
            self.input_image_2_pixmap = self.controller.numpy_to_qpixmap(self.input_image_2.input_image)
            self.input_image_2_label.setPixmap(self.input_image_2_pixmap)
            self.input_image_2_label.setScaledContents(True)
    
    def toggle_noise_checkboxes(self):
        if(self.apply_noise_checkbox.isChecked()):
            self.uniform_noise_checkbox.setDisabled(False)
            self.salt_noise_checkbox.setDisabled(False)
            self.gaussian_noise_checkbox.setDisabled(False)   
        else:
            self.uniform_noise_checkbox.setChecked(False)
            self.uniform_noise_checkbox.setDisabled(True)
            self.salt_noise_checkbox.setDisabled(True)
            self.salt_noise_checkbox.setChecked(False)
            self.gaussian_noise_checkbox.setDisabled(True)
            self.gaussian_noise_checkbox.setChecked(False)
    
    def set_output_image_source(self , index):
        if(index == 1):
            self.controller.current_output_source_index = ImageSource.IMAGE_1.value
        elif(index == 2):
            self.controller.current_output_source_index = ImageSource.IMAGE_2.value
        self.controller.set_output_image_source()
    
    def apply_uniform_noise(self):
        if(self.uniform_noise_checkbox.isChecked()):
            self.controller.apply_uniform_noise()
            
    def apply_salt_and_pepper_noise(self):
        if(self.salt_noise_checkbox.isChecked()):
            self.controller.apply_salt_and_pepper_noise()
    
    def reset_output_to_input_state(self):
        self.controller.reset_output_image_to_normal()
        self.uniform_noise_checkbox.setChecked(False)        
        self.salt_noise_checkbox.setChecked(False)        
        self.gaussian_noise_checkbox.setChecked(False)        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())