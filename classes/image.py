import cv2
import numpy as np
import random
from PyQt5.QtWidgets import QFileDialog

class Image():
    def __init__(self):
        self.input_image = None # kept untouched
        self.output_image = None # the one that will be modified by noise, filters etc.
        self.image_type = None # 'grey' or 'color' image
        self.input_image_fft = None # input image in frequency domain
        self.output_image_fft = None # output image in frequency domain

    def select_image(self):
        '''
        function to select and upload an image 
        '''
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp *.gif *.tif)", options=options)
        if file_path:
            self.input_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            self.output_image = self.input_image.copy() # a copy of the selected image is made so we can modify it without affecting the original image
            self.update_image_type(self.input_image) # update the selected image type
            
    def update_image_type(self, image):
        '''
        function that detects whether image is grey or color (rgb) and updates the image_type attribute
        '''
        # splitting the image into its 3 color channels
        r,g,b = cv2.split(image)

        # getting differences between them
        r_g = np.count_nonzero(abs(r-g))
        r_b = np.count_nonzero(abs(r-b))
        g_b = np.count_nonzero(abs(g-b))
        diff_sum = float(r_g+r_b+g_b)

        # finding ratio of diff_sum with respect to size of image
        ratio = diff_sum/image.size
        if ratio > 0.005:
            self.image_type = 'color'
        else:
            self.image_type = 'grey'
    
    def apply_noise(self, noise_type , mean = 0 , sigma = np.sqrt(0.1)):
        if noise_type == 'uniform':
            self.output_image = self.output_image / 255.0
            x, y, dimensions = self.output_image.shape

            min = 0.0
            max = 0.2

            noise = np.zeros((x, y), dtype = np.float64)
            for i in range(x):
                for j in range(y):
                    noise[i][j] = random.uniform(min, max)

            r, g, b = cv2.split(self.output_image)
            r = r + noise
            g = g + noise
            b = b + noise
            self.output_image = cv2.merge((r, g, b))
            self.output_image = np.clip(self.output_image, 0.0, 1.0)
            self.output_image = (self.output_image * 255).astype(np.uint8)

        elif noise_type == 'gaussian':
            self.output_image = self.output_image / 255.0
            x, y, dimensions = self.output_image.shape
            # mean = 0
            # variance = 0.1
            # sigma = np.sqrt(variance) # standard deviation
            noise = np.random.normal(loc = mean,
                                 scale = sigma, # standard deviation
                                 size = (x, y))
            r, g, b = cv2.split(self.output_image)
            r = r + noise
            g = g + noise
            b = b + noise
            self.output_image = cv2.merge((r, g, b))
            self.output_image = np.clip(self.output_image, 0.0, 1.0)
            self.output_image = (self.output_image * 255).astype(np.uint8)

        # note: salt & pepper type is found only in grayscale images, that's why we convert the image to grayscale first before adding the noise
        elif noise_type == 'salt_pepper':
            self.output_image = self.convert_rgb_to_gray(self.output_image)
            
            # Getting the dimensions of the image 
            row, col = self.output_image.shape 
            
            # randomly pick number of pixels (between 300 and 10000 pixls) in the image to be colored white 
            number_of_pixels = random.randint(300, 10000) 

            # add the salt and pepper noise at random positions in the image
            for i in range(number_of_pixels): 
                
                # a random y coordinate 
                y_coord=random.randint(0, row - 1) 
                
                # a random x coordinate 
                x_coord=random.randint(0, col - 1) 
                
                # color that pixel to white 
                self.output_image[y_coord][x_coord] = 255
                
            # same as above but for black pixels
            number_of_pixels = random.randint(300 , 10000) 
            for i in range(number_of_pixels): 
                
                y_coord=random.randint(0, row - 1) 
                
                x_coord=random.randint(0, col - 1) 
                
                # color that pixel to black
                self.output_image[y_coord][x_coord] = 0
    
    def convert_rgb_to_gray(self, image):
        r,g,b = cv2.split(image)
        r = 0.299 * r
        g = 0.587 * g
        b = 0.114 * b
        grey_image = r + g + b
        self.image_type = 'grey'
        
        return grey_image.astype(np.uint8)
    
    def fourier_transform(self, image):
        '''
        this function returns:
        
        1. shifted_frequency_domain_image -> which is the one to be passed on to the inverse_fourier_transform function to produce the time domain image.

        2. scaled_magnitude_image -> this one to be displayed in the GUI as the image in the frequency domain.

        Note: to do the fourier transform, the image must be in grayscale. that's why we convert it to grayscale directly in the first step.
        '''
        image = self.convert_rgb_to_gray(image)

        # compute the discrete Fourier Transform of the image. cv2.dft returns the Fourier Transform as a NumPy array.
        frequency_domain_image = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
        
        # Shift the zero-frequency component of the Fourier Transform to the center of the array because the cv2.dft() function returns the Fourier Transform with the zero-frequency component at the top-left corner of the array
        shifted_frequency_domain_image = np.fft.fftshift(frequency_domain_image)
        
        # calculate the magnitude and then take log and multiply by 20 to convert to dB
        magnitude_of_frequency_domain_image = 20*np.log(cv2.magnitude(shifted_frequency_domain_image[:,:,0],shifted_frequency_domain_image[:,:,1]))
        
        # scale the magnitude of the Fourier Transform using the cv2.normalize() function for improving the contrast of the resulting image
        scaled_magnitude_image = cv2.normalize(magnitude_of_frequency_domain_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        return shifted_frequency_domain_image, scaled_magnitude_image
    
    def inverse_fourier_transform(frequency_domain_image):
        '''
        when going from frequency domain to time domain, we need to reverse the process we did when going from time domain to frequency domain.
        '''
        shifted_frequency_image = np.fft.ifftshift(frequency_domain_image)
        time_domain_image = cv2.idft(shifted_frequency_image)
        time_domain_image = cv2.magnitude(time_domain_image[:,:,0], time_domain_image[:,:,1])
        time_domain_image = cv2.normalize(time_domain_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        return time_domain_image
    
    def apply_filter(self, filter_type, sigma = 1):
        ''' 
        apply low or high pass filter to image in the spatial domain
        we choose 3x3 kernel for each filter type
        '''
        if filter_type == 'Average':
            kernel = np.ones((3,3),np.float32)/9
            
        elif filter_type == 'Gaussian':
            x, y = np.meshgrid(np.arange(-1,2), np.arange(-1,2))  
            kernel = np.exp(-(x**2 + y**2)/(2*sigma**2))/(2*np.pi*sigma**2) 
            kernel = kernel / np.sum(kernel)    # normalization for the kernel
            
        elif filter_type == 'Median':
            padded_image = np.pad(self.output_image, pad_width = 1, mode='constant', constant_values=0)  # pad the image with frame of zeros
            for i in range(self.output_image.shape[0]):
                for j in range(self.output_image.shape[1]):
                    self.output_image[i,j] = np.median(padded_image[i:i + 3, j:j + 3])
            return
        
        elif filter_type == 'Sobel':
            pass
        
        elif filter_type == 'Roberts':
            pass
        
        elif filter_type == 'Prewitt':
            pass
        
        elif filter_type == 'Canny':
            pass
            
        self.convolve(self.output_image, kernel)
    
    def frequency_domain_low_pass_filter(shifted_fft_image):
        '''
        low pass filter blurrs the image
        '''
        rows, columns, dimensions = shifted_fft_image.shape
        print(shifted_fft_image.shape)
        center_row = rows // 2
        center_column = columns // 2

        lpf_mask = np.zeros((rows, columns, 2), np.uint8)
        lpf_mask[center_row - 70: center_row + 70, center_column - 70: center_column + 70] = 1

        filtered_fft_image = shifted_fft_image * lpf_mask
        return filtered_fft_image

    def frequency_domain_high_pass_filter(shifted_fft_image):
        '''
        high pass filter acts like an edge detector
        '''
        rows, columns, dimensions = shifted_fft_image.shape
        center_row = rows // 2
        center_column = columns // 2

        lpf_mask = np.ones((rows, columns, 2), np.uint8)
        lpf_mask[center_row - 70: center_row + 70, center_column - 70: center_column + 70] = 0

        filtered_fft_image = shifted_fft_image * lpf_mask
        return filtered_fft_image
        
    def convolve(self, image, kernel):
        '''
        implement convolution operation on the image 
        '''
        image = image.astype(np.float32)
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        padded_image = np.pad(image, pad_width=((1, 1), (1, 1), (0, 0)), mode='constant', constant_values=0) # pad the image with frame of zeros
        
        output_image = np.zeros_like(image, dtype=np.float32)
        
        for c in range(channels):
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    region = padded_image[i:i+3, j:j+3, c]
                    output_image[i, j, c] = np.sum(region * kernel)
                    
        output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        self.output_image = output_image