import cv2
import numpy as np
import streamlit as st


@st.cache
def bw_filter(img):
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    return img_gray
@st.cache
def sepia(img):
    img_sepia = img.copy()
    # Converting to RGB as sepia matrix below is for RGB.
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB) 
    img_sepia = np.array(img_sepia, dtype = np.float64)
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                    [0.349, 0.686, 0.168],
                                                    [0.272, 0.534, 0.131]]))
    # Clip values to the range [0, 255].
    img_sepia = np.clip(img_sepia, 0, 255)
    img_sepia = np.array(img_sepia, dtype = np.uint8)
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)
    return img_sepia

@st.cache
def vignette(img, level = 2):
    
    height, width = img.shape[:2]  
    
    # Generate vignette mask using Gaussian kernels.
    X_resultant_kernel = cv2.getGaussianKernel(width, width/level)
    Y_resultant_kernel = cv2.getGaussianKernel(height, height/level)
        
    # Generating resultant_kernel matrix.
    kernel = Y_resultant_kernel * X_resultant_kernel.T 
    mask = kernel / kernel.max()
    
    img_vignette = np.copy(img)
        
    # Applying the mask to each channel in the input image.
    for i in range(3):
        img_vignette[:,:,i] = img_vignette[:,:,i] * mask
    
    return img_vignette

@st.cache
def embossed_edges(img):
    
    kernel = np.array([[0, -3, -3], 
                       [3,  0, -3], 
                       [3,  3,  0]])
    
    img_emboss = cv2.filter2D(img, -1, kernel=kernel)
    return img_emboss
@st.cache
def pencil_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(gray, (3,3), 0)
    img = cv2.Laplacian(img, -1, ksize=5)
    output = 255 - img
    ret, img_sketch = cv2.threshold(output, 150, 255, cv2.THRESH_BINARY)
    return img_sketch
@st.cache
def cartoon_filter(img):
    img_color = img
    num_down=2
    num_bilateral = 7
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)

    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
    
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    gray1 = cv2.medianBlur(gray1,7)
    img_edges = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2BGR)
    img_cartoon = cv2.bitwise_and(img_color,img_edges)   
    return img_cartoon     

@st.cache
def sketch_filter(img):
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    invert_img=cv2.bitwise_not(gray1)
    blur_img = cv2.GaussianBlur(invert_img,(41,41),sigmaX=0,sigmaY=0)
    sketch_img=cv2.divide(gray1,255-blur_img, scale=256.0)
    return sketch_img
