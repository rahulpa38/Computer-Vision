## ---------------------------- ##
## 
## sample_student.py
##
## Example student submission for programming challenge. A few things: 
## 1. Before submitting, change the name of this file to your firstname_lastname.py.
## 2. Be sure not to change the name of the method below, classify.py
## 3. In this challenge, you are only permitted to import numpy and methods from 
##    the util module in this repository. Note that if you make any changes to your local 
##    util module, these won't be reflected in the util module that is imported by the 
##    auto grading algorithm. 
## 4. Anti-plagarism checks will be run on your submission
##
##
## ---------------------------- ##


import numpy as np
from math import exp
# import matplotlib.pyplot as plt 

def filter_2d(im, kernel):
    '''
    Filter an image by taking the dot product of each 
    image neighborhood with the kernel matrix.
    Args:
    im = (H x W) grayscale floating point image
    kernel = (M x N) matrix, smaller than im
    Returns: 
    (H-M+1 x W-N+1) filtered image.
    '''

    M = kernel.shape[0] 
    N = kernel.shape[1]
    H = im.shape[0]
    W = im.shape[1]
    
    filtered_image = np.zeros((H-M+1, W-N+1), dtype = 'float64')
    
    for i in range(filtered_image.shape[0]):
        for j in range(filtered_image.shape[1]):
            image_patch = im[i:i+M, j:j+N]
            filtered_image[i, j] = np.sum(np.multiply(image_patch, kernel))
            
    return filtered_image

def convert_to_grayscale(im):
    '''
    Convert color image to grayscale.
    Args: im = (nxmx3) floating point color image scaled between 0 and 1
    Returns: (nxm) floating point grayscale image scaled between 0 and 1
    '''
    return np.mean(im, axis = 2)


def make_gaussian_kernel(size, sigma):
    '''
    Create a gaussian kernel of size x size. 
    Args: 
    size = must be an odd positive number
    sigma = standard deviation of gaussian in pixels
    Returns: A floating point (size x size) guassian kernel 
    ''' 
    #Make kernel of zeros:
    kernel = np.zeros((size, size))
    
    #Handle sigma = 0 case (will result in dividing by zero below if unchecked)
    if sigma == 0:
        return kernel 
    
    #Helpful for indexing:
    k = int((size-1)/2)
    
    for i in range(size):
        for j in range(size):
            kernel[i, j] = (1/(2*np.pi*sigma**2))*exp(-((i-k)**2 + (j-k)**2)/(2*sigma**2))
            
    return kernel

gaussian_kernel = make_gaussian_kernel(11,2)

def classify(im):
    '''
    Example submission for coding challenge. 
    Args: im (nxmx3) unsigned 8-bit color image 
    Returns: One of three strings: 'brick', 'ball', or 'cylinder'  
    '''
    im = im[0:255,0:255]

    gray = convert_to_grayscale(im/255.)
    
    Kx = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]])
    
    Ky = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]])
    
    
    Gx = filter_2d(gray, Kx)
    Gy = filter_2d(gray, Ky)
    
    #Compute Gradient Magnitude and Direction:
    G_magnitude = np.sqrt(Gx**2+Gy**2)
    G_direction = np.arctan2(Gy, Gx)
    G_max = np.max(G_magnitude)
    edges = G_magnitude > (G_max*0.55)
    sum_of_values = np.sum(G_magnitude[np.where(G_magnitude > (G_max*0.55))])
    print("Gmax",G_max)
    print("Sum of Values",sum_of_values)
    
    y_coords, x_coords = np.where(edges)
    labels = ['brick', 'ball', 'cylinder']
    
    print("Length of X Coordinate",len(x_coords))
    print("sum/len(x_coords)",sum_of_values/len(x_coords))
    
    if  (sum_of_values/len(x_coords)) > 1.2 and (sum_of_values/len(x_coords)) <= 1.6:
        return labels[2]
    elif (sum_of_values/len(x_coords)) > 0 and (sum_of_values/len(x_coords)) <= 1.2:
        return labels[1]
    else:
        return labels[0]