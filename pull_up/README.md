# Pull Up Bar

### Content

- pull_up_count: Arduino code to count pull-ups with ultrasonic sensor
- `sqlite_helper.py`: A helper with some basic sqlite functions inside
- `setup.py`: Run this script in terminal to setup the database and add/edit user info
- `main.py`: The main programme. Run it after running `setup.py` 

### How to use

- Make sure you have sqlite3 installed on your device by running:
```
$ sudo apt-get install sqlite3
```
- At `3.007-Team_7/pull_up/` directory, in terminal, run:
```
$ python3 setup.py
```
- Make sure the databse and tables `Users` and `Records` are created without error. Then follow the instruction to add/edit user info or quit
- Upload pull_up_count/pull_up_count.ino to the Arduino, and keep the usb cable connected to your device
- run `main.py`