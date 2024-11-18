import os
import sys
import numpy as np
from skimage import io, filters, color
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget,
    QSlider, QPushButton, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageWindow(QWidget):
    def __init__(self, image_dir):
        super().__init__()

        self.image_path = image_dir

        # Load image
        self.image = io.imread(image_dir)

        # Window settings
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, self.image.shape[1], self.image.shape[0])

        # Create layout
        layout = QVBoxLayout()

        # Create labels for sliders
        self.gama_label = QLabel("Gamma")
        self.gama_label.setAlignment(Qt.AlignCenter)

        self.intensity_label = QLabel("Intensity")
        self.intensity_label.setAlignment(Qt.AlignCenter)

        self.brightness_label = QLabel("Brightness")
        self.brightness_label.setAlignment(Qt.AlignCenter)

        self.sigma_label = QLabel("Gaussian Blur Sigma")
        self.sigma_label.setAlignment(Qt.AlignCenter)

        # Create sliders
        self.slider_gama = QSlider(Qt.Horizontal)
        self.slider_gama.setMinimum(50)
        self.slider_gama.setMaximum(200)
        self.slider_gama.setValue(100)
        self.slider_gama.setTickInterval(1)
        self.slider_gama.valueChanged.connect(self.on_gama_slider_change)

        self.slider_intensity = QSlider(Qt.Horizontal)
        self.slider_intensity.setMinimum(50)
        self.slider_intensity.setMaximum(200)
        self.slider_intensity.setValue(100)
        self.slider_intensity.setTickInterval(1)
        self.slider_intensity.valueChanged.connect(self.on_intensity_slider_change)

        self.slider_brightness = QSlider(Qt.Horizontal)
        self.slider_brightness.setMinimum(-255)
        self.slider_brightness.setMaximum(255)
        self.slider_brightness.setValue(0)
        self.slider_brightness.setTickInterval(1)
        self.slider_brightness.valueChanged.connect(self.on_brightness_slider_change)

        self.slider_sigma = QSlider(Qt.Horizontal)
        self.slider_sigma.setMinimum(1)
        self.slider_sigma.setMaximum(50)
        self.slider_sigma.setValue(20)
        self.slider_sigma.setTickInterval(1)
        self.slider_sigma.valueChanged.connect(self.on_sigma_slider_change)

        # Create QLabel to display the image
        self.image_label = QLabel()

        # Convert NumPy array to QPixmap
        pixmap = self.numpy_to_qpixmap(self.image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # Align the image to the center

        # Create RadioButtons for filter selection
        self.radio_no_filter = QRadioButton("No Filter")
        self.radio_gaussian = QRadioButton("Gaussian Blur")
        self.radio_sobel = QRadioButton("Sobel Edges")

        # Button group (for exclusive behavior)
        self.filter_group = QButtonGroup()
        self.filter_group.addButton(self.radio_no_filter, id=0)
        self.filter_group.addButton(self.radio_gaussian, id=1)
        self.filter_group.addButton(self.radio_sobel, id=2)

        # Set action for filter change
        self.filter_group.buttonClicked.connect(self.on_filter_change)

        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.on_download_button_click)

        # Add elements to the layout
        layout.addWidget(self.gama_label)
        layout.addWidget(self.slider_gama)
        layout.addWidget(self.intensity_label)
        layout.addWidget(self.slider_intensity)
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.slider_brightness)
        layout.addWidget(self.sigma_label)
        layout.addWidget(self.slider_sigma)
        layout.addWidget(self.radio_no_filter)
        layout.addWidget(self.radio_gaussian)
        layout.addWidget(self.radio_sobel)
        layout.addWidget(self.image_label)
        layout.addWidget(self.download_button)

        # Set the layout on the QWidget
        self.setLayout(layout)

        # Update initial image
        self.gama = 1
        self.intensity = 1
        self.brightness = 0
        self.sigma = 20
        self.selected_filter = 0
        self.radio_no_filter.setChecked(True)
        self.update_image()

    def numpy_to_qpixmap(self, array):
        """
        Converts a NumPy array to QPixmap.
        If the image has only one channel, we convert it to a 3-channel image (grayscale to RGB).
        """
        if len(array.shape) == 2:  # Single channel (grayscale)
            # Convert grayscale to RGB by repeating the single channel
            array = np.stack([array] * 3, axis=-1)
        
        height, width, channels = array.shape
        bytes_per_line = channels * width
        image = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(image)

    def update_image(self):
        # Normalize the image
        normalized_image = self.image / 255.0

        # Apply gamma, intensity, and brightness corrections
        gama_corrected = np.power(normalized_image, self.gama)
        intensity_corrected = gama_corrected * self.intensity
        brightness_corrected = intensity_corrected + self.brightness
        clipped_image = np.clip(brightness_corrected, 0, 1)

        # Apply the selected filter
        if self.selected_filter == 1:  # Gaussian Blur
            filtered_image = filters.gaussian(clipped_image, sigma=self.sigma / 10, channel_axis=-1)
        elif self.selected_filter == 2:  # Sobel Edges
            if len(clipped_image.shape) == 3:  # RGB image
                gray_image = color.rgb2gray(clipped_image)
            else:  # Grayscale image
                gray_image = clipped_image
            sobel_image = filters.sobel(gray_image)
            filtered_image = np.stack([sobel_image] * 3, axis=-1)  # Recreate 3 channels for display
        else:  # No Filter
            filtered_image = clipped_image

        # Save the modified image
        self.modified_image = (filtered_image * 255).astype(np.uint8)

        # Convert to QPixmap and display
        pixmap = self.numpy_to_qpixmap(self.modified_image)
        self.image_label.setPixmap(pixmap)

    def on_gama_slider_change(self, value):
        self.gama = value / 100.0
        self.update_image()

    def on_intensity_slider_change(self, value):
        self.intensity = value / 100.0
        self.update_image()

    def on_brightness_slider_change(self, value):
        self.brightness = value / 255.0
        self.update_image()

    def on_sigma_slider_change(self, value):
        self.sigma = value
        self.update_image()

    def on_filter_change(self, button):
        self.selected_filter = self.filter_group.checkedId()
        self.update_image()

    def on_download_button_click(self):
        save_dir = os.path.join(os.getcwd(), 'modified_' + os.path.basename(self.image_path))
        io.imsave(save_dir, self.modified_image)
        print(f'Saved to: {save_dir}')

# Initialize the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow(sys.argv[1])
    window.show()
    sys.exit(app.exec_())
