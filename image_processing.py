import cv2
import numpy as np


def transform_image(image_path):
    # Load the input image
    image = cv2.imread(image_path)
    
    cv2.waitKey(0)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using Canny edge detector
    edges = cv2.Canny(blur, 50, 150)

    # Find contours in the edge map
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area and select the largest one (assuming it's the paper)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = contours[0]

    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Check if the image is flipped or inverted
    top_left = approx[0, 0]
    top_right = approx[1, 0]
    bottom_right = approx[2, 0]
    bottom_left = approx[3, 0]

    flipped = False
    inverted = False
    if top_left[1] > bottom_left[1]:
        flipped = True
    if top_left[0] > top_right[0]:
        inverted = True

    # Calculate the perspective transformation matrix
    # if flipped and inverted:
    #     pts = np.float32([[800, 0], [0, 0], [0, 800], [800, 800]])
    # elif flipped:
    #     pts = np.float32([[800, 800], [0, 800], [0, 0], [800, 0]])
    # elif inverted:
    pts = np.float32([[0, 800], [800, 800], [800, 0], [0, 0]])
    # else:
    #     pts = np.float32([[0, 0], [800, 0], [800, 800], [0, 800]])
    #     
    

    approx = np.float32(approx.reshape((-1, 2)))
    matrix = cv2.getPerspectiveTransform(approx, pts)

    # Apply the perspective transformation to the original image
    output = cv2.warpPerspective(image, matrix, (800, 800))
    # Rotate the output image 90 degrees clockwise

    rows, cols = output.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
    output = cv2.warpAffine(output, rotation_matrix, (cols, rows))

    # Save the output image
    cv2.imwrite('output_image.jpg', output)
    
# transform_image('schedule.jpg')