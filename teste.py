''' import cv2
import numpy as np

cap = cv2.VideoCapture(1)

cap.set(3, 1280)
cap.set(4, 720)

while True:
    ret, img = cap.read()

    img2 = img.copy()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
    teste = 0
    if np.any(thresh[50, 50]):
        teste += 1
    print(teste)
    branco = np.sum(thresh == 255)
    preto = np.sum(thresh == 0)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        # Internal = !=
        # External = ==
        if hierarchy[0][i][3] != -1:
            if preto < 140000 and preto > 120000:
                cv2.putText(img2, "Achou", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 1)
                cv2.drawContours(img2, contours, i, (0, 255, 0), -1)
            else:
                cv2.putText(img2, "Não Achou", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1)
                cv2.drawContours(img2, contours, i, (0, 0, 255), -1)

    cv2.imshow("Contours", img2)
    cv2.waitKey(1) '''
''' import cv2
import numpy as np

cap = cv2.VideoCapture(1)


while True:
    ret, img = cap.read()
    img2 = img.copy()
    blur = cv2.blur(img, (8, 8))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    filtro = cv2.filter2D(blur, -1, (3, 3))
    gradient = cv2.morphologyEx(filtro, cv2.MORPH_GRADIENT, kernel)
    cv2.imshow("g", gradient)
    opening = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("c", opening)
    opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
    cv2.imshow("o", opening)

    canny = cv2.Canny(opening, 127,
                      cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(
        canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        # Internal = !=
        # External = ==
        if hierarchy[0][i][3] == -1:
            cv2.drawContours(img2, contours, i, (0, 255, 0), 2)

    print(img[1:2, 2:3][0][0])
    cv2.imshow("b", canny)
    cv2.imshow("Cannys", img2)
    cv2.waitKey(1) '''


import cv2
import numpy as np
cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

colors = ()


def selectColor(event, x, y, flags, param):
    global colors
    if event == cv2.EVENT_LBUTTONDOWN:
        colors = img[y, x]

        print("RGB Value at ({},{}):{} ".format(x, y, colors))


while True:
    pixels = 0
    ret, img = cap.read()

    img2 = img.copy()
    if colors != ():
        lower = (colors[0]/2, colors[1]/2, colors[2]/2)
        upper = (colors[0]/2+colors[0], colors[1] /
                 2+colors[1], colors[2]/2+colors[2])
        mask1 = cv2.inRange(img, lower, upper)
        pixels = np.sum(mask1)
        cv2.imshow("mask", mask1)
    print(pixels)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
    branco = np.sum(thresh == 255)
    preto = np.sum(thresh == 0)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        # Internal = !=
        # External = ==
        if hierarchy[0][i][3] != -1:
            if pixels > 30000000 and pixels < 40000000:
                cv2.putText(img2, "Achou", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 1)
                cv2.drawContours(img2, contours, i, (0, 255, 0), -1)
            else:
                cv2.putText(img2, "Não Achou", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1)
                cv2.drawContours(img2, contours, i, (0, 0, 255), -1)

    cv2.namedWindow('Life2CodingRGB')
    cv2.setMouseCallback('Life2CodingRGB', selectColor)
    cv2.imshow("Life2CodingRGB", img)
    cv2.imshow("a", img2)
    cv2.waitKey(1)
