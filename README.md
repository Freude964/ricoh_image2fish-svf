
# Cylindrical image to sky fisheye images for RICOH

A simple program that transforms bar charts into fish-eye views facing the sky, and calculates their Sky View Factor (SVF). 
It offers two methods: equidistant projection and equal-area projection, and allows customization of the threshold value for calculating SVF.
 This program has been verified on the RICOH THETA S, and theoretically, any image with a width/height ratio of 2 can be processed correctly.

# Theory
![enter image description here](https://www.researchgate.net/publication/330767706/figure/fig4/AS:721301899591680@1548983182642/Transformation-from-a-cylindrical-equidistant-image-to-fisheye-images-of-equidistant.jpg)
  
This is a Python implementation of the projection method described in the paper：
**Sky view factor measurement by using a spherical camera**
If you use this code for your research, please cite:
https://doi.org/10.2480/agrmet.D-18-00027
# How to Use
**1. Make sure to install the required dependencies.**
`pip install -r requirements.txt`
**2. Place the images you want to process in the same folder with the .py file.**
The code supports .png and .jpg files. Ensure the image size is 4Lx2L (width x height).
**3. Image Process**
The program accepts two arguments.
>  `projection_type` offers two options: "equalarea" and "equaldis", representing equal-area projection and equidistant projection respectively. If not specified, the default is "equalarea". 
>  `threshold` accepts a floating-point number between 0 and 1, representing the threshold for binarization (black and white) of terrain and sky. The default value is 0.55.

**Example:**`python image2fish.py --projection_type equalarea --threshold 0.55`


# Others
This program runs on the CPU. Depending on the performance of the CPU, each image may take 1 minute or more to process. Please be patient.


