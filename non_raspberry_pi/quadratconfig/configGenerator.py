#!/usr/bin/python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
import time
from PIL import Image
import io

#Variablen
fenster_name = "OpenCV Quadraterkennung"
kreis_durchmesser_mm = 7
min_threshold = 0
max_threshold = 100
oben_links = (400,150)
unten_rechts = (900,600)
kernel = np.ones((5, 5), np.uint8)
gauss_faktor = 0
gauss_matrix = (7,7)
config = configparser.ConfigParser()
maxCorners = 300 #Anzahl zu erkennenden Kanten
qualityLevel = 0.03 #je höher desto genauer
minDistance = 10 #mindeste Distanz zwischen Punkten

# ----------------------------------- Main Code -----------------------
def main(argv):
    cam = cv2.VideoCapture(0);
    while cam.isOpened():
        ret, img = cam.read()
        filename = argv[0]
        #img = cv2.imread(filename, cv2.IMREAD_COLOR)

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)
        #ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            #rect = cv2.minAreaRect(contours[0])
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

            x_values = [] #Listen für x und y werte um die passenden rauszusuchen
            y_values = []

            for i in approx:
                x_values.append(i[0][0])
                y_values.append(i[0][1])

            if area > 400:
                cv2.drawContours(img, [approx] ,0,(0,0,255),3)
                cv2.circle(img, (min(x_values), min(y_values)), 2, (255,255,0), 2) #oben links
                cv2.circle(img, (max(x_values), min(y_values)), 2, (255,255,0), 2) #oben rechts
                cv2.circle(img, (min(x_values), max(y_values)), 2, (255,255,0), 2) #unten links
                cv2.circle(img, (max(x_values), max(y_values)), 2, (255,255,0), 2) #unten rechts

                x_seite = math.sqrt((min(x_values) - max(x_values))**2 + (min(y_values) - max(y_values))**2)
                y_seite = math.sqrt((min(x_values) - min(x_values))**2 + (min(y_values) - max(y_values))**2)

                cv2.putText(img, str(round(x_seite,2)) + "px X_Seite" , (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
                cv2.putText(img, str(round(y_seite,2)) + "px Y_Seite" , (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

        cv2.namedWindow(fenster_name, 1)
        cv2.imshow(fenster_name, img)
        key = cv2.waitKey(1)
        # Wenn ESC gedrückt wird, wird  das Programm beendet
        if key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])