import numpy as np
import matplotlib.pyplot as plt

class StatisticsVisualization():
    def __init__(self , input_image_1 , input_image_2 , output_image, labels):
        self.input_image_1 = input_image_1
        self.input_image_2 = input_image_2
        self.output_image = output_image

    def plot_histogram_and_pdf(self, image, labels):
        for label in labels:
            histogram = np.zeros(256)
            for pixel in image.ravel():  
                histogram[pixel] += 1

            pdf = histogram / histogram.sum()
            plt.figure(figsize=(10, 4))
            plt.subplot(1, 2, 1)
            plt.bar(range(256), histogram, color='blue', width=5)
            plt.title("Histogram")
            plt.xlabel("Intensity")
            plt.ylabel("Count")

            plt.subplot(1, 2, 2)
            plt.plot(pdf, color='blue')
            plt.title("PDF")
            plt.xlabel("Intensity")
            plt.ylabel("Probability")

            plt.show()