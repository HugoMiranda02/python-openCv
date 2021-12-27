import cv2


def Life2CodingRGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # checks mouse moves
        colorsBGR = img[y, x]
        # Reversing the OpenCV BGR format to RGB format
        colorsRGB = tuple(reversed(colorsBGR))
        print("RGB Value at ({},{}):{} ".format(x, y, colorsRGB))


# Create a window and set Mousecallback to a function for that window
cv2.namedWindow('Life2CodingRGB')
cv2.setMouseCallback('Life2CodingRGB', Life2CodingRGB)
# Do until esc pressed
cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    cv2.imshow('Life2CodingRGB', img)
    cv2.waitKey(1)
# if esc is pressed, close all windows.
cv2.destroyAllWindows()
