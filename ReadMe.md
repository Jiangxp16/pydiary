# **Diary Application**
A pure application for diary writing based on pyside6.
All data save to "diary.db" in program path and could export to excel file.
(Press Ctrl-I/Ctrl-B for fun)

<img src="diary.png" width="500" height="300">

## **Build with pyinstaller**
Use your own distpath.
Build one-file mode which easily to share.
```
pyinstaller build_f.spec -y --distpath "E:\Program Files\Diary"
```
Or build a directory. Attention that it will empty original directory. It would be better to control file size if built with multiple exes in this mode. Delete unused modules and dlls after building.
```
pyinstaller build_d.spec -y --distpath "E:\Program Files\Diary"
```

## **Dependencies**
Developed with python 3.10.6.
```
pyside6==6.6.2
pillow==10.2.0
openpyxl=3.1.2
pyinstaller=6.4.0
holidays==0.44
sxtwl==2.0.6
```

## **Config**
Build config.ini in program path to replace default configuration, usable configurations:
```
[global]
db_name=diary.db
first_day_of_week=7
language=zh
multi_thread=1

[style]
font=Times New Roman,Kaiti
font_size=18
logo=style/logo.png
qss=style/default.qss
```