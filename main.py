import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow , QPushButton , QFrame , QLabel , QVBoxLayout , QCheckBox , QComboBox , QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from classes.image import Image
from classes.controller import Controller
from classes.ImageEnum import ImageSource
from classes.statisticsVisualization import HistogramCanvas , CDFCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.gaussian_noise_checkbox.stateChanged.connect(self.apply_gaussian_noise)
        
        # Adding Gaussian mean and sigma
        self.gaussian_mean_text = self.findChild(QLineEdit , "meanInput")
        self.gaussian_mean_text.textChanged.connect(self.set_gaussian_mean)
        
        self.gaussian_mean = 0
        self.gaussian_std = np.sqrt(0.1)
        
        self.gaussian_std_text = self.findChild(QLineEdit , "stdInput")
        self.gaussian_std_text.textChanged.connect(self.set_gaussian_std)
        
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
        
        # Initialize rgb to grey button
        self.rgb2grey_button = self.findChild(QPushButton , "toGreyScale")
        self.rgb2grey_button.clicked.connect(self.to_grey_scale)
        
        # Initializing the low pass time domain filter combobox
        self.low_pass_time_domain_filters_combobox = self.findChild(QComboBox , "lowPassCombobox")
        self.low_pass_time_domain_filters_combobox.currentIndexChanged.connect(self.apply_low_pass_filter_time_domain)
        
        # Initialize gaussian filter sigma input
        self.gaussian_filter_sigma = 1
        self.gaussian_filter_sigma_input = self.findChild(QLineEdit,"lowPassGaussianInput")
        self.gaussian_filter_sigma_input.textChanged.connect(self.set_gaussian_filter_sigma)
        
        # Histogram of Input Image 1
        self.input_image_1_histogram_canvas = HistogramCanvas()
        input_image_1_histogram_frame = self.findChild(QFrame , "input01HistogramFrame")
        self.input_image_1_histogram_layout = QVBoxLayout(input_image_1_histogram_frame)
        self.input_image_1_histogram_layout.addWidget(self.input_image_1_histogram_canvas)
        
        # CDF of Input Image 1
        self.input_image_1_cdf_canvas = CDFCanvas()
        input_image_1_cdf_frame = self.findChild(QFrame , "input01DistributionFrame")
        self.input_image_1_cdf_layout = QVBoxLayout(input_image_1_cdf_frame)
        self.input_image_1_cdf_layout.addWidget(self.input_image_1_cdf_canvas)
        
        # Histogram of Input Image 2
        self.input_image_2_histogram_canvas = HistogramCanvas()
        input_image_2_histogram_frame = self.findChild(QFrame , "input02HistogramFrame")
        layout = QVBoxLayout(input_image_2_histogram_frame)
        layout.addWidget(self.input_image_2_histogram_canvas)
        
        # CDF of Input Image 2
        self.input_image_2_cdf_canvas = CDFCanvas()
        input_image_2_cdf_frame = self.findChild(QFrame , "input02DistributionFrame")
        layout = QVBoxLayout(input_image_2_cdf_frame)
        layout.addWidget(self.input_image_2_cdf_canvas)
        
        # Histogram of Output Image
        self.output_image_histogram_canvas = HistogramCanvas()
        input_output_image_histogram_frame = self.findChild(QFrame , "outputHistogramFrame")
        layout = QVBoxLayout(input_output_image_histogram_frame)
        layout.addWidget(self.output_image_histogram_canvas)
        
        # CDF of Output  Image
        self.output_image_cdf_canvas = CDFCanvas()
        output_image_cdf_frame = self.findChild(QFrame , "outputDistributionFrame")
        layout = QVBoxLayout(output_image_cdf_frame)
        layout.addWidget(self.output_image_cdf_canvas)
        
        # Initializing Edge Detectors in time domain
        self.edge_detectors_time_domain_filters_combobox = self.findChild(QComboBox , "edgeDetectorsCombobox")
        self.edge_detectors_time_domain_filters_combobox.currentIndexChanged.connect(self.apply_edge_detector_time_domain)
        
        # Initializing Controller
        self.controller = Controller(self.input_image_1 , self.input_image_2 , self.output_image , self.output_image_label , self.input_image_1_histogram_canvas, self.input_image_1_cdf_canvas , 
                                    self.input_image_2_histogram_canvas , self.input_image_2_cdf_canvas , self.output_image_histogram_canvas , self.output_image_cdf_canvas)
        
        
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
            self.controller.apply_noise('uniform')
            
    def apply_salt_and_pepper_noise(self):
        if(self.salt_noise_checkbox.isChecked()):
            self.controller.apply_noise('salt_pepper')
    
    def apply_gaussian_noise(self):
        if(self.gaussian_noise_checkbox.isChecked()):
            self.controller.apply_noise('gaussian', self.gaussian_mean , self.gaussian_std)
    
    def set_gaussian_mean(self , text):
        if (text == "" or text == " " or '-' in text ):
            return
        self.gaussian_mean = float(text)
        self.apply_gaussian_noise()
    
    def set_gaussian_std(self , text):
        if (text == "" or text == " " or '-' in text):
            return
        self.gaussian_std = float(text)
        self.apply_gaussian_noise()
    
    def reset_output_to_input_state(self):
        self.controller.reset_output_image_to_normal()
        self.uniform_noise_checkbox.setChecked(False)        
        self.salt_noise_checkbox.setChecked(False)        
        self.gaussian_noise_checkbox.setChecked(False)        
    
    def to_grey_scale(self):
        self.controller.rgb2grey()
    
    def set_gaussian_filter_sigma(self , text):
        if (text == "" or text == " " or '-' in text):
            return
        self.gaussian_filter_sigma = float(text)
        
    def apply_low_pass_filter_time_domain(self ,index):
        if(index == 0):
            return
        if (index == 1):
            filter_type = "Average"
        elif (index == 2):
            filter_type = "Gaussian"
        elif (index == 3):
            filter_type = "Median"    
        self.controller.apply_time_domain_low_pass(filter_type ,self.gaussian_filter_sigma)
    
    def apply_edge_detector_time_domain(self , index):
        if(index == 0):
            return
        if (index == 1):
            edge_detector_filter_type = "Sobel"
        elif (index == 2):
            edge_detector_filter_type = "Roberts"
        elif (index == 3):
            edge_detector_filter_type = "Prewitt"
        elif (index == 4):
            edge_detector_filter_type = "Canny"
        self.controller.apply_edge_detector_time_domain(edge_detector_filter_type)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())