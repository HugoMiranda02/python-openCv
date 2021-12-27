import numpy as np
import cv2
import os

MainProperties = {
    "ferramenta": {
        "id": -1,
        "index": 0,
        "save_preview": False,
    }
}

MainFilters = {
    "gray": False,
    "roi": False,
    "blur": False,
    "edges": {
        "enable": False,
        "kernel-x": 3,
        "kernel-y": 3,
        "kernelF-x": 3,
        "kernelF-y": 3,
        "thresh1": 127,
        "thresh2": 255,
        "external": True,
        "Internal": False
    },
    "pixels": False,
}


class vision:
    def __init__(self):
        # Inicia a câmera
        self.video = cv2.VideoCapture(0)
        # Seta a resolução para 640 x 360
        self.video.set(3, 3264)
        self.video.set(4, 2448)
        self.roi_img = []
        self.final_img = []

    def updateValues(self):
        self.blur = MainFilters["blur"]
        self.roi = MainFilters["roi"]
        self.edges = MainFilters["edges"]

    def rgb_to_hsv(r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        s = 0 if mx == 0 else (df/mx)*100
        v = mx*100
        return (h, s, v)

    def countPixels(self, img):
        x, y = self.pixels
        bgr_value = img[y, x]
        rgb = tuple(reversed(bgr_value))
        img = cv2.cvtColor(cv2.COLOR_BGR2HSV)
        lower = (int(rgb[0] - (rgb[0] * .25)), int(rgb[1] -
                 (rgb[1] * .25)), int(rgb[2] - (rgb[2] * .25)))
        upper = (int(rgb[0] + (rgb[0] * .25)), int(rgb[1] +
                 (rgb[1] * .25)), int(rgb[2] + (rgb[2] * .25)))

        Hl, Sl, Vl = self.rgb_to_hsv(lower[0], lower[1], lower[2])
        Hu, Su, Vu = self.rgb_to_hsv(lower[0], lower[1], lower[2])

        lower = (Hl, Sl, Vl)
        upper = (Hu, Su, Vu)

        mask1 = cv2.inRange(img, lower, upper)

        return np.sum(mask1)

    def apply_blur(self, img):
        blur = int(float(self.blur))
        ksize = int(blur) if int(blur) % 2 == 1 else int(blur) + 1
        blur = cv2.GaussianBlur(
            img, (int(ksize), int(ksize)), 0)
        return blur.copy()

    def reduceNoiseAndDetect(self, img):
        kernelX = MainFilters["edges"]["kernel-x"]
        kernelY = MainFilters["edges"]["kernel-y"]
        kernelFX = MainFilters["edges"]["kernelF-x"]
        kernelFY = MainFilters["edges"]["kernelf-y"]
        thresh1 = MainFilters["edges"]["thresh1"]
        thresh2 = MainFilters["edges"]["thresh2"]
        kernel = (kernelX, kernelY)
        kernelF = (kernelFX, kernelFY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        filtro = cv2.filter2D(img, -1, kernelF)
        gradient = cv2.morphologyEx(filtro, cv2.MORPH_GRADIENT, kernel)
        opening = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

        canny = cv2.Canny(opening, thresh1,
                          thresh2)

        contours, hierarchy = cv2.findContours(
            canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, hierarchy)

    def getROI(self, img):
        x, y, w, h = self.roi
        # Transforma de string para inteiro
        x = int(float(x))
        y = int(float(y))
        w = int(float(w))
        h = int(float(h))

        # Converte para a resolução correta
        x = int((3264 * x) / 720)
        y = int((2448 * y) / 480)
        w = int((3264 * w) / 720)
        h = int((2448 * h) / 480)

        # Seleciona o Ridge of Interest da imagem
        ROI = img[y:y+h, x:x+w]
        return ROI.copy()

    def view(self):
        self.updateValues()
        if self.final_img == []:
            return ''
        img = self.final_img
        final = img.copy()
        if self.roi:
            ROI = self.getROI(final)
            self.roi_img = ROI.copy()

            final = ROI.copy()
            if float(self.blur) > 0:
                final = self.apply_blur(ROI)
            if self.edges:
                contours, hierarchy = self.reduceNoiseAndDetect(final)
                for i in range(len(contours)):
                    # Internal = !=
                    # External = ==
                    if hierarchy[0][i][3] != -1:
                        cv2.drawContours(final, contours, i, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', final)
        return jpeg.tobytes()

    def trigger(self):
        ret, img = self.video.read()
        self.final_img = img.copy()

    def savePreview(self, img):
        if int(MainProperties["ferramenta"]["id"]) > 0:
            if not os.path.exists(f"static/imgs/{MainProperties['ferramenta']['id']}"):
                os.mkdir(f"static/imgs/{MainProperties['ferramenta']['id']}")
            cv2.imwrite(
                f"static/imgs/{MainProperties['ferramenta']['id']}/1.jpeg", img)

    def preview(self):
        self.updateValues()
        _, img = self.video.read()
        final = img.copy()
        if self.roi:
            ROI = self.getROI(final)
            self.roi_img = ROI.copy()

            final = ROI.copy()
            if float(self.blur) > 0:
                final = self.apply_blur(final)
            if self.edges:
                contours, hierarchy = self.reduceNoiseAndDetect(final)
                for i in range(len(contours)):
                    # Internal = !=
                    # External = ==
                    if hierarchy[0][i][3] == -1:
                        cv2.drawContours(final, contours, i, (0, 255, 0), 2)

            if MainProperties["ferramenta"]["save_preview"]:
                MainProperties["ferramenta"]["save_preview"] = False
                self.savePreview(final)

        _, jpeg = cv2.imencode('.jpg', final)
        return jpeg.tobytes()
