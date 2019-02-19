# OpenCV
OpenCV Gesicht/Kantenerkennung - Python 
#author = Jonathan Evertz

Programm einfach mit 
    python3 opencv.py --argumente
starten.
Hierbei sind folgende Argumente (auch in Kombination) möglich:

Modus:

--image Ist das Argument gesetzt, wird man aufgefordert ein Bildnamen einzugeben um dieses auf z.B. Kanten durchsuchen zu lassen. BEACHTE, dass man zusätzlich noch               ein Argument mindestens für die Operation setzen muss. 

Operationen: 

--face Wendet Gesichtserkennung an
--border Erstellt eine Kantenerkennung
--circle Erkennt Kreise und deren Mittelpunkt

Beispiel:

python3 opencv.py --image --circle --border Erkennt in einem Bild Kreise und Kanten
python3 opencv.py --circle --border Benutz die Kamera um Live Kreise und Kanten zu erkennen
