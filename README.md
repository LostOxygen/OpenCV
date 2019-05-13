# Readme für RoboSchalt mit OpenCV (Python)
### Dependecies:
(bestenfalls in dieser Reihenfolge installieren)
*Es wird zwingend Python3 benötigt!*
+ DirMngr : **sudo apt-get install dirmngr**
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ [NumPy](http://www.numpy.org/): **sudo pip3 install numpy**
+ [OpenCV](http://www.codebind.com/cpp-tutorial/install-opencv-ubuntu-cpp/) (vor dem kompilieren libfaac s.u. installieren!)
+ zusätzlich für [V4L2 Codec](https://www.raspberrypi.org/forums/viewtopic.php?t=62364):  **sudo modprobe bcm2835-v4l2**

Alle für den RPI benötigten Dateien sind **ausschließlich** im Ordner *raspberry_pi* zu finden.

Grundsätzlich werden alle Skripte mit **./skriptname.py** oder **python3 skriptname.py** gestartet, lediglich *webservice.py* und der *TCP/IP Server* erfordern **sudo**.

### Libfaac für Debian (Stretch)
Läuft der Raspberrypi unter Debian/Raspbian, so gibt es das Paket Libfaac nicht in den offiziellen Repo's. Deswegen:
```shell
 sudo nano /etc/apt/sources.list
 deb http://www.deb-multimedia.org/ stretch main non-free hinzufügen
 sudo apt-get install debian-keyring
 gpg --keyserver pgp.mit.edu --recv-keys 1F41B907
 gpg --armor --export 1F41B907 | apt-key add
 sudo apt-get update (ggf. zwischendurch öfters)
 sudo apt-get install deb-multimedia-keyring
 sudo apt-get update
 sudo apt-get install libfaac-dev
```
### Troubleshooting
Überprüfen ob OpenCV richtig installiert wurde:
```python
  import cv2
  cv2.__version__
```
Falls das Modul cv2 in python3 nicht gefunden werden kann:
```shell
  /usr/local/lib/python2.x/dist-packages
```
nach Ordner *cv2* durchsuchen und ggf. nach
```shell
  /usr/local/lib/python3.x/dist-packages
```
kopieren.
