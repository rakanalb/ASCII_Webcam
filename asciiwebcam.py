import cv2
import numpy as np

# Take in webcam input
cap = cv2.VideoCapture(0)

width, height = 1000, 1000
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# cell dimensions defined in pixels
cell_width, cell_height = 10, 15
new_width, new_height = int(width / cell_width), int(height / cell_height)
new_dimensions = (new_width, new_height)

# ASCII characters that are 'brightest' to 'darkest'. 
# Used as guide to replicate image intensity
chars = " .,-~:;=!*#$@"

norm = 255 / len(chars)
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.4

def matrix(image):
    global matrix_window
    
    # Lay the foundation for the ASCII characters
    matrix_window = np.zeros((height, width, 3), np.uint8)
    
    small_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_NEAREST)
    gray_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
    
    # Find ASCII Character & color for each cell
    for i in range(new_height):
        for j in range(new_width):
            intensity = gray_image[i, j]
            
            # Find which ASCII character fits this cell based on greyscale intensity
            char_index = int(intensity / norm)
            
            color = small_image[i, j]
            B = int(color[0])
            G = int(color[1])
            R = int(color[2])
            
            char = chars[char_index]
            cv2.putText(matrix_window, char, (j * cell_width + 5, i * cell_height + 12), font, font_size, (B, G, R), 1)

while True:
    ret, frame = cap.read()
    
    # Flip camera to mirror the webcam from user's perspective
    frame = cv2.flip(frame, 180)    
    
    matrix(frame)
    cv2.imshow('result', matrix_window)
    
    # if escape key pressed, stop program
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
    