import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow , QPushButton , QStackedWidget ,QFrame , QLabel , QVBoxLayout, QHBoxLayout , QCheckBox , QComboBox , QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_functions.compile_qrc import compile_qrc
from classes.image import Image
from classes.controller import Controller
from classes.ImageEnum import ImageSource , Channel
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
        
        # Histogram Stack of Input Image 1
        self.input_image_1_histogram_stack = self.findChild(QStackedWidget , "histogramInput01Stack")
        
        # Histogram of Input Image 1
        self.input_image_1_red_histogram_canvas = HistogramCanvas()
        self.input_image_1_green_histogram_canvas = HistogramCanvas()
        self.input_image_1_blue_histogram_canvas = HistogramCanvas()
        
        self.input_image_1_histogram_frame_red = self.findChild(QFrame , "rInput01HistogramFrame")
        self.input_image_1_histogram_frame_green = self.findChild(QFrame , "gInput01HistogramFrame")
        self.input_image_1_histogram_frame_blue = self.findChild(QFrame , "bInput01HistogramFrame")
        
        self.input_image_1_histogram_layout_red = QVBoxLayout(self.input_image_1_histogram_frame_red)
        self.input_image_1_histogram_layout_red.addWidget(self.input_image_1_red_histogram_canvas)
        
        self.input_image_1_histogram_layout_green = QVBoxLayout(self.input_image_1_histogram_frame_green)
        self.input_image_1_histogram_layout_green.addWidget(self.input_image_1_green_histogram_canvas)
        
        self.input_image_1_histogram_layout_blue = QVBoxLayout(self.input_image_1_histogram_frame_blue)
        self.input_image_1_histogram_layout_blue.addWidget(self.input_image_1_blue_histogram_canvas)
        
        self.input_image_1_histogram_red_button = self.findChild(QPushButton , "rButtonInput01")
        self.input_image_1_histogram_green_button = self.findChild(QPushButton , "gButtonInput01")
        self.input_image_1_histogram_blue_button = self.findChild(QPushButton , "bButtonInput01")
        
        self.input_image_1_histogram_red_button.pressed.connect(self.change_histogram1_to_red_color_channel)
        self.input_image_1_histogram_green_button.pressed.connect(self.change_histogram1_to_green_color_channel)
        self.input_image_1_histogram_blue_button.pressed.connect(self.change_histogram1_to_blue_color_channel)
        
        # PDF , CDF of Input Image 1
        self.input_image_1_cdf_canvas = CDFCanvas()
        self.input_image_1_pdf_canvas = CDFCanvas()
        
        input_image_1_cdf_frame = self.findChild(QFrame , "cdfInput01DistributionFrame")
        self.input_image_1_cdf_layout = QVBoxLayout(input_image_1_cdf_frame)
        self.input_image_1_cdf_layout.addWidget(self.input_image_1_cdf_canvas)
        
        input_image_1_pdf_frame = self.findChild(QFrame , "pdfInput01DistributionFrame")
        self.input_image_1_pdf_layout = QVBoxLayout(input_image_1_pdf_frame)
        self.input_image_1_pdf_layout.addWidget(self.input_image_1_pdf_canvas)
        
        # Histogram stack of Input Image 2
        self.input_image_2_histogram_stack = self.findChild(QStackedWidget , "histogramInput02Stack")
        
        # Histogram of Input Image 2
        self.input_image_2_red_histogram_canvas = HistogramCanvas()
        self.input_image_2_green_histogram_canvas = HistogramCanvas()
        self.input_image_2_blue_histogram_canvas = HistogramCanvas()
        
        input_image_2_red_histogram_frame = self.findChild(QFrame , "rInput02HistogramFrame")
        input_image_2_green_histogram_frame = self.findChild(QFrame , "gInput02HistogramFrame")
        input_image_2_blue_histogram_frame = self.findChild(QFrame , "bInput02HistogramFrame")
        
        self.input_image_2_histogram_layout_red = QVBoxLayout(input_image_2_red_histogram_frame)
        self.input_image_2_histogram_layout_red.addWidget(self.input_image_2_red_histogram_canvas)
        
        self.input_image_2_histogram_layout_green = QVBoxLayout(input_image_2_green_histogram_frame)
        self.input_image_2_histogram_layout_green.addWidget(self.input_image_2_green_histogram_canvas)
        
        self.input_image_2_histogram_layout_blue = QVBoxLayout(input_image_2_blue_histogram_frame)
        self.input_image_2_histogram_layout_blue.addWidget(self.input_image_2_blue_histogram_canvas)
        
        self.input_image_2_histogram_red_button = self.findChild(QPushButton , "rButtonInput02")
        self.input_image_2_histogram_green_button = self.findChild(QPushButton , "gButtonInput02")
        self.input_image_2_histogram_blue_button = self.findChild(QPushButton , "bButtonInput02")
        
        self.input_image_2_histogram_red_button.pressed.connect(self.change_histogram2_to_red_color_channel)
        self.input_image_2_histogram_green_button.pressed.connect(self.change_histogram2_to_green_color_channel)
        self.input_image_2_histogram_blue_button.pressed.connect(self.change_histogram2_to_blue_color_channel)
        
        # CDF of Input Image 2
        self.input_image_2_cdf_canvas = CDFCanvas()
        input_image_2_cdf_frame = self.findChild(QFrame , "input02DistributionFrame")
        layout = QVBoxLayout(input_image_2_cdf_frame)
        layout.addWidget(self.input_image_2_cdf_canvas)
        
        # Histogram stack of Output Image
        self.output_image_histogram_stack = self.findChild(QStackedWidget , "histogramOutputStack")
        
        # Histogram of Output Image
        self.output_red_histogram_canvas = HistogramCanvas()
        self.output_green_histogram_canvas = HistogramCanvas()
        self.output_blue_histogram_canvas = HistogramCanvas()
        
        output_image_red_histogram_frame = self.findChild(QFrame , "rOutputHistogramFrame")
        output_image_green_histogram_frame = self.findChild(QFrame , "gOutputHistogramFrame")
        output_image_blue_histogram_frame = self.findChild(QFrame , "bOutputHistogramFrame")
        
        self.output_image_histogram_layout_red = QVBoxLayout(output_image_red_histogram_frame)
        self.output_image_histogram_layout_red.addWidget(self.output_red_histogram_canvas)
        
        self.output_image_histogram_layout_green = QVBoxLayout(output_image_green_histogram_frame)
        self.output_image_histogram_layout_green.addWidget(self.output_green_histogram_canvas)
        
        self.output_image_histogram_layout_blue = QVBoxLayout(output_image_blue_histogram_frame)
        self.output_image_histogram_layout_blue.addWidget(self.output_blue_histogram_canvas)
        
        self.output_image_histogram_red_button = self.findChild(QPushButton , "rButtonOutput")
        self.output_image_histogram_green_button = self.findChild(QPushButton , "gButtonOutput")
        self.output_image_histogram_blue_button = self.findChild(QPushButton , "bButtonOutput")
        
        self.output_image_histogram_red_button.pressed.connect(self.change_histogram_output_to_red_color_channel)
        self.output_image_histogram_green_button.pressed.connect(self.change_histogram_output_to_green_color_channel)
        self.output_image_histogram_blue_button.pressed.connect(self.change_histogram_output_to_blue_color_channel)
        
        
        # CDF of Output  Image
        self.output_image_cdf_canvas = CDFCanvas()
        output_image_cdf_frame = self.findChild(QFrame , "outputDistributionFrame")
        layout = QVBoxLayout(output_image_cdf_frame)
        layout.addWidget(self.output_image_cdf_canvas)
        
        # Initializing Edge Detectors in time domain
        self.edge_detectors_time_domain_filters_combobox = self.findChild(QComboBox , "edgeDetectorsCombobox")
        self.edge_detectors_time_domain_filters_combobox.currentIndexChanged.connect(self.apply_edge_detector_time_domain)
        
        # Initializing Hybrid Image
        self.input_image_1_hybrid_component_combobox = self.findChild(QComboBox , "input01HybridCombobox")
        self.input_image_2_hybrid_component_combobox = self.findChild(QComboBox , "input02HybridCombobox")
        self.hybrid_image_checkbox = self.findChild(QCheckBox , "hybridCheckbox")
        
        self.input_image_1_hybrid_component_combobox.setCurrentIndex(1)
        self.input_image_1_hybrid_component_combobox.currentIndexChanged.connect(self.set_input_image_1_freq_component)
        
        
        self.input_image_2_hybrid_component_combobox.setCurrentIndex(2)
        self.input_image_2_hybrid_component_combobox.currentIndexChanged.connect(self.set_input_image_2_freq_component)
        
        self.hybrid_image_checkbox.stateChanged.connect(self.apply_hybrid_image)
        self.hybrid_image = Image()
        
        self.low_freq_image = self.input_image_1.input_image
        self.high_freq_image = self.input_image_2.input_image

        # Initializing Local Thresholding
        self.local_threshold_window_size = self.findChild(QLineEdit , "localThresholdSize")
        self.local_threshold_window_size.textChanged.connect(self.set_local_threshold_window_size)

        self.local_threshold_constant = self.findChild(QLineEdit , "localThresholdContsant")
        self.local_threshold_constant.textChanged.connect(self.set_local_threshold_constant)

        self.applyButtonLocal = self.findChild(QPushButton , "applyButtonLocal")
        self.applyButtonLocal.clicked.connect(self.apply_local_thresholding)

        # Initializing Global Thresholding
        self.global_threshold_value = self.findChild(QLineEdit , "globalThresholdValue")
        self.global_threshold_value.textChanged.connect(self.set_global_threshold_value)

        self.applyButtonGlobal = self.findChild(QPushButton , "applyButtonGlobal")
        self.applyButtonGlobal.clicked.connect(self.apply_global_thresholding)
        
        # Initialize Frequency Domain Filters
        self.frequency_domain_filters_combobox = self.findChild(QComboBox , "frequencyDomainCombobox")
        self.frequency_domain_filters_combobox.currentIndexChanged.connect(self.change_shown_freq_filters_params)
        
        self.frequency_domain_filters_stacked_widget = self.findChild(QStackedWidget , "frequencyDomainFiltersStack")
        
        # Ideal Freq Filter
        self.ideal_filter_radius_line_edit = self.findChild(QLineEdit , "idealFilterRadiusInput")
        self.ideal_filter_radius_line_edit.textChanged.connect(self.set_ideal_filter_radius)
        self.ideal_filter_radius = 70
        self.ideal_filter_type = None
        self.apply_ideal_frequency_domain_filters_button = self.findChild(QPushButton , "idealFilterButton")
        self.apply_ideal_frequency_domain_filters_button.pressed.connect(self.apply_ideal_frequency_domain_filters)
        
        # ButterWorth Freq filter
        self.butter_order_line_edit = self.findChild(QLineEdit , "butterworthOrderInput")
        self.butter_order_line_edit.textChanged.connect(self.set_butter_filter_order)
        self.butter_cutoff_line_edit = self.findChild(QLineEdit , "butterworthCutoffFrequencyInput")
        self.butter_cutoff_line_edit.textChanged.connect(self.set_butter_filter_cutoff)
        self.butter_filter_type = None
        self.butter_filter_cutoff = 10
        self.butter_filter_order = 1
        self.apply_butter_frequency_domain_filters_button = self.findChild(QPushButton , "butterworthButton")
        self.apply_butter_frequency_domain_filters_button.pressed.connect(self.apply_butter_frequency_domain_filters)
        
        # Gaussian Freq filter
        self.gaussian_cutoff_line_edit = self.findChild(QLineEdit , "gaussianCutoffFrequencyInput")
        self.gaussian_cutoff_line_edit.textChanged.connect(self.set_gaussian_filter_cutoff)
        self.gaussian_filter_type = None
        self.gaussian_filter_cutoff = 10
        self.apply_gaussian_frequency_domain_filters_button = self.findChild(QPushButton , "gaussianFrequencyButton")
        self.apply_gaussian_frequency_domain_filters_button.pressed.connect(self.apply_gaussian_frequency_domain_filters)
        
        # Initialize Removable Frames
        self.input_image_1_freq_comp_frame = self.findChild(QFrame , "input01HybridFrame")
        self.input_image_2_freq_comp_frame = self.findChild(QFrame , "input02HybridFrame")
        self.output_image_freq_comp_frame = self.findChild(QFrame , "outputHybridFrame")
        self.input_image_1_freq_comp_frame.hide()
        self.input_image_2_freq_comp_frame.hide()
        self.output_image_freq_comp_frame.hide()
        
        # Initialize Kernel Size Choice
        self.filter_size_combobox = self.findChild(QComboBox , "kernelSizeCombobox")
        self.filter_size_combobox.setCurrentIndex(1)
        self.filter_size_combobox.currentIndexChanged.connect(self.change_filter_size)
        self.filter_size = 3
        
        self.filter_type = None
        self.edge_detector_filter_type = None
        
        # Initializing Histogram Equalization Button
        self.histogram_equalization_button = self.findChild(QPushButton , "normalize")
        self.histogram_equalization_button.pressed.connect(self.apply_histogram_equalization)
        
        # Initializing Controller
        self.controller = Controller(self.input_image_1 , self.input_image_2 , self.output_image , self.output_image_label ,
                                    self.input_image_1_red_histogram_canvas,self.input_image_1_green_histogram_canvas,self.input_image_1_blue_histogram_canvas,
                                    self.input_image_1_cdf_canvas , self.input_image_1_pdf_canvas ,
                                    self.input_image_2_red_histogram_canvas ,self.input_image_2_green_histogram_canvas , self.input_image_2_blue_histogram_canvas,
                                    self.input_image_2_cdf_canvas ,
                                    self.output_red_histogram_canvas ,self.output_green_histogram_canvas,self.output_blue_histogram_canvas,
                                    self.output_image_cdf_canvas,
                                    self.hybrid_image , self.low_freq_image , self.high_freq_image)
        
        
    def browse_image_input_1(self):
        self.controller.browse_image_input_1()
        if (len(self.input_image_1.input_image)):
            self.input_image_1_pixmap = self.controller.numpy_to_qpixmap(self.input_image_1.input_image)
            self.input_image_1_label.setPixmap(self.input_image_1_pixmap)
            self.input_image_1_label.setScaledContents(True)
            if(self.input_image_1_hybrid_component_combobox.currentIndex() == 1):
                self.low_freq_image = self.input_image_1.input_image
            elif (self.input_image_1_hybrid_component_combobox.currentIndex() == 2):
                self.high_freq_image = self.input_image_1.input_image
            self.apply_hybrid_image()
            self.output_image_selector_combobox.setCurrentIndex(1)
                
    def browse_image_input_2(self):
        self.controller.browse_image_input_2()
        if (len(self.input_image_2.input_image)):
            self.input_image_2_pixmap = self.controller.numpy_to_qpixmap(self.input_image_2.input_image)
            self.input_image_2_label.setPixmap(self.input_image_2_pixmap)
            self.input_image_2_label.setScaledContents(True)
            if(self.input_image_2_hybrid_component_combobox.currentIndex() == 1):
                self.low_freq_image = self.input_image_2.input_image
            elif (self.input_image_2_hybrid_component_combobox.currentIndex() == 2):
                self.high_freq_image = self.input_image_2.input_image
            self.apply_hybrid_image()
            self.output_image_selector_combobox.setCurrentIndex(2)
                
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
        if (text == "" or text == " " or '-' in text  or text.isalpha()):
            return
        self.gaussian_mean = float(text)
        self.apply_gaussian_noise()
    
    def set_gaussian_std(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
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
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.gaussian_filter_sigma = float(text)
        
    def apply_low_pass_filter_time_domain(self ,index):
        if(index == 0):
            return
        if (index == 1):
            self.filter_type = "Average"
        elif (index == 2):
            self.filter_type = "Gaussian"
        elif (index == 3):
            self.filter_type = "Median"    
        self.controller.apply_time_domain_low_pass(self.filter_type ,self.filter_size,self.gaussian_filter_sigma)
    
    def apply_edge_detector_time_domain(self , index):
        if(index == 0):
            return
        if (index == 1):
            self.edge_detector_filter_type = "Sobel"
        elif (index == 2):
            self.edge_detector_filter_type = "Roberts"
        elif (index == 3):
            self.edge_detector_filter_type = "Prewitt"
        elif (index == 4):
            self.edge_detector_filter_type = "Canny"
        self.controller.apply_edge_detector_time_domain(self.edge_detector_filter_type , self.filter_size)
    
    def set_input_image_1_freq_component(self , index):
        if(index == 1):
            self.input_image_2_hybrid_component_combobox.setCurrentIndex(2)
            self.low_freq_image = self.input_image_1.input_image
            self.high_freq_image = self.input_image_2.input_image
            
        elif(index == 2):
            self.input_image_2_hybrid_component_combobox.setCurrentIndex(1)
            self.low_freq_image = self.input_image_2.input_image
            self.high_freq_image = self.input_image_1.input_image
        self.apply_hybrid_image()
        
    def set_input_image_2_freq_component(self , index):
        if(index == 1):
            self.input_image_1_hybrid_component_combobox.setCurrentIndex(2)
            self.low_freq_image = self.input_image_2.input_image
            self.high_freq_image = self.input_image_1.input_image
            
        elif(index == 2):
            self.input_image_1_hybrid_component_combobox.setCurrentIndex(1)
            self.low_freq_image = self.input_image_1.input_image
            self.high_freq_image = self.input_image_2.input_image
        self.apply_hybrid_image()

    def apply_hybrid_image(self):
        if(self.hybrid_image_checkbox.isChecked()):
            self.input_image_1_freq_comp_frame.show()
            self.input_image_2_freq_comp_frame.show()
            self.output_image_freq_comp_frame.show()
            if(self.low_freq_image is None or self.high_freq_image is None):
                return
            self.controller.hybrid_image_mode = True
            self.controller.current_output_source_index = 0
            self.controller.apply_hybrid_image(self.low_freq_image , self.high_freq_image)
            self.output_image_selector_combobox.setCurrentIndex(1)
            self.output_image_selector_combobox.setCurrentIndex(0)
        else:
            self.input_image_1_freq_comp_frame.hide()
            self.input_image_2_freq_comp_frame.hide()
            self.output_image_freq_comp_frame.hide()
            if(self.low_freq_image is None or self.high_freq_image is None):
                return
            self.controller.hybrid_image_mode = False
            self.controller.current_output_source_index = 1
            self.output_image_selector_combobox.setCurrentIndex(1)
            self.controller.reset_output_image_to_normal()

    def set_local_threshold_window_size(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.local_threshold_window_size = float(text)

    def set_local_threshold_constant(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.local_threshold_constant = float(text)

    def apply_local_thresholding(self):
        self.controller.apply_local_thresholding(self.local_threshold_window_size , self.local_threshold_constant)

    def set_global_threshold_value(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.global_threshold_value = float(text)

    def apply_global_thresholding(self):
        self.controller.apply_global_thresholding(self.global_threshold_value)
    
    def change_shown_freq_filters_params(self , index):
        if(index == 0):
            return
        if(index == 1):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(0)
            self.ideal_filter_type = 'high'
        if(index == 2):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(0)
            self.ideal_filter_type = 'low'
        if(index == 3):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(1)
            self.butter_filter_type = 'high'
        if(index == 4):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(1)
            self.butter_filter_type = 'low'
        if(index == 5):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(2)
            self.gaussian_filter_type = 'high'
        if(index == 6):
            self.frequency_domain_filters_stacked_widget.setCurrentIndex(2)
            self.gaussian_filter_type = 'low'
            
    def change_filter_size(self , index):
        if(index == 0):
            return
        elif(index == 1):
            self.filter_size = 3
        elif (index == 2):
            self.filter_size = 5
        if(self.filter_type != None):
            self.controller.apply_time_domain_low_pass(self.filter_type , self.filter_size ,self.gaussian_filter_sigma)
        if(self.edge_detector_filter_type != None):
            self.controller.apply_edge_detector_time_domain(self.edge_detector_filter_type , self.filter_size)
    
    def set_ideal_filter_radius(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.ideal_filter_radius = float(text)
    
    
    def set_butter_filter_cutoff(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.butter_filter_cutoff = float(text)
    
    def set_butter_filter_order(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.butter_filter_order = int(text)
    
    def set_gaussian_filter_cutoff(self , text):
        if (text == "" or text == " " or '-' in text or text.isalpha()):
            return
        self.gaussian_filter_cutoff = float(text)
        
    def apply_ideal_frequency_domain_filters(self):
        self.controller.apply_ideal_freq_filters(self.ideal_filter_type , self.ideal_filter_radius)
    
    def apply_butter_frequency_domain_filters(self):
        self.controller.apply_butter_freq_filters(self.butter_filter_type , self.butter_filter_cutoff , self.butter_filter_order)
    
    def apply_gaussian_frequency_domain_filters(self):
        self.controller.apply_gaussian_freq_filters(self.gaussian_filter_type , self.gaussian_filter_cutoff)
    
    def apply_histogram_equalization(self):
        self.controller.apply_histogram_equalization()
    
    def change_histogram1_to_red_color_channel(self):
        self.input_image_1_histogram_stack.setCurrentIndex(Channel.RED.value)
    
    def change_histogram1_to_green_color_channel(self):
        self.input_image_1_histogram_stack.setCurrentIndex(Channel.GREEN.value)
    
    def change_histogram1_to_blue_color_channel(self):
        self.input_image_1_histogram_stack.setCurrentIndex(Channel.BLUE.value)
    
    def change_histogram2_to_red_color_channel(self):
        self.input_image_2_histogram_stack.setCurrentIndex(Channel.RED.value)
    
    def change_histogram2_to_green_color_channel(self):
        self.input_image_2_histogram_stack.setCurrentIndex(Channel.GREEN.value)
    
    def change_histogram2_to_blue_color_channel(self):
        self.input_image_2_histogram_stack.setCurrentIndex(Channel.BLUE.value)
    
    def change_histogram_output_to_red_color_channel(self):
        self.output_image_histogram_stack.setCurrentIndex(Channel.RED.value)
    
    def change_histogram_output_to_green_color_channel(self):
        self.output_image_histogram_stack.setCurrentIndex(Channel.GREEN.value)
    
    def change_histogram_output_to_blue_color_channel(self):
        self.output_image_histogram_stack.setCurrentIndex(Channel.BLUE.value)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())