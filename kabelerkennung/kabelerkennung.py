#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt
from matplotlib import pyplot as plt

#Variablen
fenster_name = "Kabelerkenung"
mittelpunkt = (int(1920/2), int(1080/2))
config_test = True
kreis_durchmesser_mm = 7
threshold_val = 100
threshold_max = 300
oben_links = (400,150)
unten_rechts = (900,600)
maxCorners = 300 #Anzahl zu erkennenden Kanten
qualityLevel = 0.03 #je höher desto genauer
minDistance = 10 #mindeste Distanz zwischen Punkten

# ----------- Config einlesen und überprüfen --------------------------
config = configparser.ConfigParser()
test = Path('config.ini')
if test.is_file():
    print('Config Datei gefunden')
    config.read('config.ini')

else:
    print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen!')
    config_test = False

kreis_durchmesser_pixel = float(config['KREISERKENNUNG']['durchmesserkreisinpixel']) #fragt Wert aus Config File ab

if kreis_durchmesser_pixel == 0:
    kreis_durchmesser_pixel = 1
    print("kreis_durchmesser_pixel war 0 und wurde auf 1 gesetzt")

umrechnung_pixel_mm = kreis_durchmesser_mm / kreis_durchmesser_pixel #Rechnet mm pro Pixel aus

# ----------------------------------- Main Code -----------------------

def main(argv):
    filename = argv[0]
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    if img is None:
        print("Fehler bei Laden der Datei: " + filename + "!\n")
        return -1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 1)
    blur = cv2.bilateralFilter(blur, 11, 17, 17)
    blur = cv2.Canny(blur, 30, 120)
    ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
    #ret, thresh = cv2.threshold(blur, threshold_val, threshold_max, cv2.THRESH_BINARY) #Threshold generieren
    contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Konturen suchen

    corners = cv2.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance)
    #corners = np.int0(corners)

    min_xy = (1000,1000) #temp Var zum finden von punkt ganz oben_links
    if corners is not None:
        for i in corners:
            x,y = i.ravel()
            if x <= 1100: #zeichnet nur Relevante Punkte
                cv2.circle(img, (x,y), 2, (0,0,255), 2)
            if x < min_xy[0]: #guckt nach kleinstem x wert
                min_xy = (x,y)

    #berechnet Distanz
    dist = math.sqrt((min_xy[0] - min_xy[0])**2 + (min_xy[1] - mittelpunkt[1])**2)

#----------- optische Ausgabe --------------------------
    cv2.circle(img, min_xy, 2, (0,255,0), 2) #zeichnet punkt ganz links
    cv2.line(img, min_xy, (min_xy[0], mittelpunkt[1]), (255,255,0), 2) #zeichnet linie von punkt nach oben
    #zeichnet Mittelpunkt und Linie nach links
    cv2.circle(img, mittelpunkt, 2, (255,255,0), 2)
    cv2.line(img, mittelpunkt, (min_xy[0],mittelpunkt[1]), (255,255,0), 2)
    cv2.line(img, mittelpunkt, min_xy, (255,255,0), 2)
    #erzeugt Text mit Pixelangabe
    cv2.putText(img, str(round(dist, 2)) + "px diff." , (min_xy[0],mittelpunkt[1]), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
    #Konturen zeichnen
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
#-------------------------------------------------------

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, img)
    cv2.waitKey(0)


    print("Distanz: " + str(round(umrechnung_pixel_mm * dist)) + "mm")
    #cv2.imwrite("bild.jpg", img) #speichert ein Bild
    plt.imshow(img), plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])