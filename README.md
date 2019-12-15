# REMATCH <a name="rematch"></a>
A 3.007-Introduction to Design Project featuring Pong game with pulling ropes# 3.007 F05 DESIGN TEAM 7

Authors:
 - Kevin Ma Yuchen
 - Lui Yan Le 
 - Hazel Xing Yunqing
 - Princeton Poh Jin Heng 
 - Jordan Chan 

## Table of Contents <a name="table-of-contents"></a>
- [REMATCH](#rematch)
    - [Table of Contents](#table-of-contents)
    - [Repo Content](#repo-content)
    - [Introduction](#introduction)
        - [Poster](#poster)
        - [Video](#video)
    - [How to use](#how-to-use)
    - [Components](#components)
        - [System Diagram](#system-diagram)
        - [Electronics](#electronics)
        - [Mechanical](#mechanical)
        - [Software](#software)
    - [Trouble Shooting & FAQ](trouble-shooting-&-faq)
    - [Future improvements](#future-improvements)

## Repo Content <a name="repo-content"></a>
- `ball.py`: ball class in pygame
- `paddle.py`: paddle class in pygame
- `main.py`: The main game script. You can run it both on a normal computer or the arcade console we made
- `i2c_encoder`: Arduino code for encoders using i2c
- `past_codes`: Things that we have have tried before but are no longer used

## Introduction <a name="introduction"></a>
REMATCH is a 3.007-Introduction to Design Project by Cohort 5 Team 7 of SUTD Class of 2022. It is a arcade game console that enables people to play the classic game Pong with the motion of pulling ropes.

### Poster <a name="poster"></a>
find the poster in `assets`
### Video <a name="video"></a>
https://youtu.be/wE_V6qiuwjU

## How to use <a name="how-to-use"></a>
1. Clone this repository to the computer/RPi
2. In the terminal, run`$ pip3 install pygame`
3. Make sure all the connections are stable if you are using an RPi
4. Check your i2c connection by the command `$ i2cdetect -y 1`, You should be able to see 04 and 05 appear in the second line among a lot of dashes
5. Go to the root directory of this repository, and run `$ python3 main.py`
6. Quite the game by closing the window or pressing "x" on your keyboard

## Components <a name="components"></a>

### System Diagram <a name="system-diagram"></a>
to be updated

### Electronics <a name="electronics"></a>

#### Raspberry Pi 4B

- To set up an RPi 4, follow this tutorial: https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up 
  note that when preparing your sd card, download the version that supports **offline installation** as you might not be able to connect to school wifi when installing.


- To connect to school wifi (PEAP-Enterprise) or school ethernet (IEEE 802.1X), follow this tutorial compiled by **Kevinskwk**:
https://github.com/Kevinskwk/Misc/blob/master/RaspberryPi/RPi4_Wifi_Configuration.md 

#### Encoders
- Due to limited budget, we used ir sensor modules as encoders. there are 12 sectors in black and white on the pulley. The two ir sensors are placed at an angle of 165 degrees, creating a 90 degree phase difference of the ir sensors' signals. With the phase difference, the encoders can detect the direction of rotation, and the precition is doubled.
- The STL file can be found in the `assets` folder.

#### Arduino Nano
- We used one Arduino Nano for each encoder, two in total.
- The encoders are connected to digital pins 2 and 3 that support the function `attachInterrupt()`
- The Arduinos are connected to the RPi via i2c. The code for the Arduinos can be found in the folder `i2c_encoder`

### Mechanical <a name="mechanical"></a>
to be updated

### Software <a name="software"></a>

#### Prerequisites
- Make sure you have `Pygame` installed
- On RPi, make sure you have the libraries `smbus` and `RPi`. Then make sure the buttons and LEDs connected properly. Make sure the i2c connection from the Arduinos to the RPi is stable.

#### Pygame
- The game is writen in Python, using Pygame library.
- The files `ball.py` and `paddle.py` contain the ball and paddle classes respectively
- The main game programme is in `main.py`. You can run it on our arcade console with encoders and buttons to achieve best experience. Alternatively, you can directly run it on any computer with the prerequesites installed. Do run from the terminal in the direction of this repo to avoid any error.

## Trouble Shooting & FAQ <a name="trouble-shooting-&-faq"></a>
to be updated

## Future improvements <a name="future-improvements"></a>
- Change into proper encoders
- Make a physical Pong game without a monitor (if we have money and time!)
- MORE LEDS