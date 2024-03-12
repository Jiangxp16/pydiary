# **Diary Application**
A pure application for diary writing based on pyside6.
All data save to "diary.db" in program path and could export to excel file.

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
del "E:\Program Files\Diary\Diary\_internal\PySide6\opengl32sw.dll"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\translations"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PIL"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\plugins\generic"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\plugins\iconengines"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\plugins\networkinformation"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\plugins\platforminputcontexts"
rmdir /s /q "E:\Program Files\Diary\Diary\_internal\PySide6\plugins\tls"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6OpenGL.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6Network.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6Pdf.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6Qml.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6QmlModels.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6Quick.dll"
del "E:\Program Files\Diary\Diary\_internal\PySide6\QtNetwork.pyd"
del "E:\Program Files\Diary\Diary\_internal\PySide6\Qt6VirtualKeyboard.dll"
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

[style]
font=Times New Roman,Kaiti
font_size=18
```