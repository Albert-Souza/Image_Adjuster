# Image_Adjuster

A Python application designed to enable users to apply adjustments and filters in real-time.

## Features
- **Gamma Correction**: Adjust the image's gamma to enhance or reduce brightness.
- **Intensity Adjustment**: Scale the image's overall intensity.
- **Brightness Adjustment**: Modify the brightness of the image.
- **Gaussian Blur**: Apply a blur effect to the image using the Gaussian filter.
- **Sobel Edge Detection**: Detect edges in the image using the Sobel filter.
- **Real-time Preview**: Adjust the image and instantly see the effects.
- **Download Option**: Save the modified image to your local system.

## Requirements
To run the tool, make sure you have the following dependencies installed:

- Python
- PyQt5
- NumPy
- scikit-image

You can install the required dependencies using `pip`:

```bash
pip install PyQt5 numpy scikit-image
```

## Usage

```bash
python image_adjuster.py example_image.png
```
