# Image Enhancer Studio

A comprehensive toolkit for image processing and enhancement that supports both grayscale and color images. This PyQt5-based desktop application provides a user-friendly interface for applying various image processing techniques, from basic noise manipulation to advanced frequency domain filtering and edge detection.

## Features

### 1. Additive Noise
- **Uniform Noise**: Add uniformly distributed random noise to images
- **Gaussian Noise**: Apply Gaussian distributed noise with customizable mean and standard deviation parameters
- **Salt & Pepper Noise**: Add impulse noise with random black and white pixels

### 2. Noise Filtering
- **Average Filter**: Smooth images using mean filtering with customizable kernel sizes
- **Gaussian Filter**: Apply Gaussian blur with adjustable sigma parameter for controlled smoothing
- **Median Filter**: Remove noise while preserving edges using median filtering

### 3. Edge Detection
- **Sobel Operator**: Detect edges using Sobel gradient filters (3x3 and 5x5 kernels)
- **Roberts Cross-Gradient**: Apply Roberts edge detection with cross-gradient operators
- **Prewitt Operator**: Edge detection using Prewitt gradient filters
- **Canny Edge Detection**: Advanced edge detection with automatic threshold selection

### 4. Histogram Analysis and Visualization
- **RGB Histogram Display**: Visualize intensity distribution for Red, Green, and Blue channels
- **Distribution Curves**: Generate and display Probability Density Function (PDF) and Cumulative Distribution Function (CDF) curves
- **Real-time Updates**: Dynamic histogram updates as images are processed

### 5. Histogram Equalization
- Enhance contrast for grayscale images

### 6. Image Normalization
- **Intensity Normalization**: Normalize pixel intensities to specified ranges (default 0-255)
- **Dynamic Range Enhancement**: Improve image contrast through pixel value redistribution

### 7. Thresholding
- **Global Thresholding**: Convert images to binary using a global threshold value
- **Local/Adaptive Thresholding**: Apply adaptive thresholding with customizable block size and constant parameters

### 8. Color Processing
- **RGB to Grayscale Conversion**: Transform color images to grayscale while preserving luminance information
- **Individual Channel Analysis**: Separate and analyze Red, Green, and Blue channels independently
- **Channel-specific Histograms**: Generate histograms and cumulative distributions for each color channel

### 9. Frequency Domain Filtering
- **High Pass Filters**: Edge enhancement and sharpening using Ideal, Butterworth, and Gaussian high-pass filters
- **Low Pass Filters**: Image smoothing and noise reduction with Ideal, Butterworth, and Gaussian low-pass filters
- **Customizable Parameters**: Adjustable cutoff frequencies and filter orders

### 10. Hybrid Images
- **Image Fusion**: Create hybrid images by combining low-frequency components from one image with high-frequency components from another
- **Dual Image Processing**: Support for processing and combining two input images simultaneously

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Youssef-Abo-El-Ela/Image-Enhancer-Studio.git
   cd Image-Enhancer-Studio
   ```

2. **Install required dependencies:**
   ```bash
   pip install PyQt5 opencv-python numpy matplotlib
   ```

## Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Basic workflow:**
   - Load one or two images using the browse buttons
   - Select desired processing options from the interface
   - Choose from various noise types, filters, and enhancement techniques
   - View real-time histograms and distribution curves
   - Apply edge detection or frequency domain operations
   - Create hybrid images by combining two input images

3. **Available processing options:**
   - Use checkboxes to enable/disable noise addition
   - Select filter types and sizes from dropdown menus
   - Adjust parameters like sigma for Gaussian operations
   - Choose between different edge detection algorithms
   - Apply global or local thresholding with custom parameters

## Results

Processed images and their corresponding histograms are displayed in real-time within the application interface. The tool provides:
- Side-by-side comparison of original and processed images
- Interactive histogram displays for all color channels
- PDF and CDF curve visualizations

## Sample Images

The `data/` directory contains various test images including:
- Standard test images (Lena, Mandrill, Peppers)
- Natural images (Cat, Dog, Lake, Living room)
- Technical images (Cameraman, Jetplane, House)

## Preview

![GUI Screenshot 1](assets/GUI%20screenshot2.png)
![GUI Screenshot 2](assets/GUI%20screenshot1.png)

## Contributors <a name = "Contributors"></a>
<table>
  <tr>
    <td align="center">
    <a href="https://github.com/Youssef-Abo-El-Ela" target="_black">
    <img src="https://avatars.githubusercontent.com/u/125592387?v=4" width="150px;" alt="Youssef Aboelela"/>
    <br />
    <sub><b>Youssef Aboelela</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/karreemm" target="_black">
    <img src="https://avatars.githubusercontent.com/u/116344832?v=4" width="150px;" alt="Kareem Abdel Nabi"/>
    <br />
    <sub><b>Kareem Abdel nabi</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/aliyounis33" target="_black">
    <img src="https://avatars.githubusercontent.com/u/125222093?v=4" width="150px;" alt="Ali Younis"/>
    <br />
    <sub><b>Ali Younis</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/louai111" target="_black">
    <img src="https://avatars.githubusercontent.com/u/79408256?v=4" width="150px;" alt="Louai Khaled"/>
    <br />
    <sub><b>Louai Khaled</b></sub></a>
    </td>
      </tr>
</table>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
