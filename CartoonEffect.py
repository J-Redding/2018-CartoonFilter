#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, cv2

def main(argv):
	original_image = argv[0]
	#Edge detection and enhancement
	edge_mask = cv2.imread(original_image)
	edge_mask = cv2.cvtColor(edge_mask, cv2.COLOR_RGB2GRAY)
	#Apply median blur first to smooth picture and reduce noise
	#The blur is applied in a 7x7 neighbourhood
	edge_mask = cv2.medianBlur(edge_mask, 7)
	#Use an adaptive threshold to detect edges
	#The threshold value is the weighted mean of values in a 9x9 area
	edge_mask = cv2.adaptiveThreshold(edge_mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)

	#Colour version colour homogenisation
	colour_image = cv2.imread(original_image)
	#Apply the bilateral filter 10 times in a 10x10 neighbourhood
	for i in range(10):
		#SigmaColor and SigmaSpace of 10 works best
		#Gives colours saturation, without making them blur together
		colour_image = cv2.bilateralFilter(colour_image, 10, 10, 10)

	#Convert edge mask back to colour, and combine the versions of the image
	edge_mask = cv2.cvtColor(edge_mask, cv2.COLOR_GRAY2RGB)
	colour_image = cv2.bitwise_and(colour_image, edge_mask)
	cv2.imwrite(argv[1], colour_image)

main(sys.argv[1:])