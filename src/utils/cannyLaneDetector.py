"""
Author : Abdoulaye Diallo <abdoulayediallo338@gmail.com>
This file contains an implementation of a Lane detector 
based on the Canny process. 
"""

# === Import necessary libraries ===

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# === Helper class definition ===

class helperFunction:
    """
    This class contains helper methods for the CannyLaneDetector.
    """

    def __init__(self):
        print("=== Helper Function initialized ===")

    def createGaussianKernel(self, sigma: float) -> np.ndarray:
        """
        Creates a normalized 2D Gaussian kernel.

        Parameters
        ----------
        sigma : float
            Standard deviation of the Gaussian.

        Returns
        -------
        kernel : np.ndarray
            A 2D Gaussian kernel.
        """
        kernel_size = int(2 * np.ceil(sigma) + 1)
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.float64)
        center = kernel_size // 2

        for y in range(kernel_size):
            for x in range(kernel_size):
                dx = x - center
                dy = y - center
                kernel[y, x] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(
                    -(dx ** 2 + dy ** 2) / (2 * sigma ** 2)
                )

        kernel /= np.sum(kernel)
        return kernel

# === Canny class definition ===


class cannyLaneDetector:
    """
    This class contains methods and attributes for building
    a proper Canny edge/lane Detector. To help my
    understanding of the problem, I will implement a scratch
    version of a method then use a library which might contains
    an optimized version of what I wrote.
    """

    def __init__(
        self, gradThresh: float, firstThresh: float, secondThresh: float
    ) -> None:
        """
        Initialisation function.
        Params:
        -------
        imgPath (str):
            Image path
        gradThresh (float):
            a threshold for the gradient intensity
        firstThresh (float):
            lower threshold for the hysterisis thresholding
        secondThresh (float):
         upper threshold for the hysterisis thresholding

        Returns:
        ------
        None
        """
        self.gradThresh = gradThresh
        self.firstThresh = firstThresh
        self.secondThresh = secondThresh
        self.utils = helperFunction()

    def readImg(self, imgPath: str) -> np.ndarray:
        """
        Read and load the image given the image path
        stored in the attributes `self.imgPath`.
        Params:
        -------
        None
        Returns:
        --------
        I (np.ndarray):
            Matrix containing the image information.
        """
        try:
            img = cv.imread(imgPath)
            if img is None:
                raise FileNotFoundError(f"Image not found or failed to load:{imgPath}")
            return img
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            return None

    def rgbToGrayScratch(self, img: np.ndarray) -> np.ndarray:
        """
        Convert an RGB image to grayscale manually.
        Supports only 3-channel RGB or single-channel grayscale images.

        Parameters:
        -----------
        img : np.ndarray or list
            Input image, either a list or Numpy array.

        Returns:
        --------
        np.ndarray
            Grayscale image.

        Raises:
        -------
        ValueError
            If input does not have 2 or 3 dimensions,
            or not 3 channels in the last dimension.
        """
        if isinstance(img, list):
            img = np.array(img)

        if not isinstance(img, np.ndarray):
            raise TypeError(
                "Input must be a Numpy array or a list convertible to a Numpy array."
            )

        if img.ndim == 3:
            r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 3]
            imgGray = 0.2989 * r + 0.5870 * g + 0.1140 * b
            return imgGray.astype(np.float32)

        elif img.ndim == 2:
            return img.astype(np.float32)
        else:
            raise ValueError(
                "Input image must be either a 2D grayscale imaege or a 3D RGB image."
            )

    def rgbToGray(self, img: np.ndarray) -> np.ndarray:
        """
        Convert an RGB image to grayscale using OpenCV
        method.
        """
        try:
            if img is None:
                raise ValueError("Input image is None")
            grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            return grayImg
        except cv.error as ce:
            print(f"[OpenCV Error] {ce}")
        except Exception as e:
            print(f"[Unexpected Error] {e}")

    def applyGaussianBlurScratch(self, img: np.ndarray, sigma: float) -> np.ndarray:
        """
        Apply Gaussian blur on a grayscale image.
        """
        if img.ndim != 2:
            raise ValueError("Input image must be a grayscale image. Nothing else.")

        kernel = self.utils.createGaussianKernel(sigma)
        return kernel
