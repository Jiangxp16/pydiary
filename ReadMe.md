# **Diary Application**
A pure application for diary writing based on pyside6.
All data save to "diary.db" in program path and could export to excel file.

<img src="diary.png" width="500" height="300">

## **Build with pyinstaller**
Use your own distpath.
```
pyinstaller -F -w core/start.py --distpath "E:\Program Files\Diary" -n Diary -i style\logo.png --add-data "style\*;.\style"
```
or
```
pyinstaller Diary.spec -y --distpath "E:\Program Files\Diary"
```

## **Dependencies**
Developed with python 3.10.6.
```
pyside6==6.6.2
pillow==10.2.0
lunardate=0.2.2
openpyxl=3.1.2
pyinstaller=6.4.0
```

## **Config**
Build config.ini in program path to replace default configuration:
```
[global]
db_name=diary.db
first_day_of_week=7

[style]
font=Times New Roman,Kaiti
font_size=18
```