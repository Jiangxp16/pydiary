# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['core\\start.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\style\\*', '.\\style')],
    hiddenimports=['holidays.countries'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PIL'],
    noarchive=False,
)


# exclude unused files
to_exclude = {"opengl", "qtqml", "qtquick", "qtsql", "qtweb", "qt63d", "qt3d",
              "qttest", "qtsvg", "qt6charts", "qt6lab", "qt6qml", "qt6quick",
              "qt6web", "qt6test", "qt6svg", "qt6sensor", "qtnfc", "qtbluetooth",
              "qt6nfc", "qt6serial", "qt6virtual", "qmltooling", "qt6pdf",
              "qwebp.dll", "qjpeg.dll", "qtiff.dll",
              "pyside6\\translations", "pyside6\\resources", "pyside6\\qml"
              "plugins\\generic", "plugins\\sensors", "plugins\\tls",
              "plugins\\virtualkeyboard", "plugins\\networkinformation",
              "plugins\\platforminputcontexts",
              "plugins\\imageformats",
              # "qt6network", "qtnetwork",
              "api-ms-win", "msvcp140", "vcruntime140", "ucrtbase",
              "PIL", "pillow", "_ssl", "libssl", "qminimal"
              }
print("****************************************")
to_keep = []
for (dest, source, kind) in a.binaries:
    include = True
    for obj in to_exclude:
        if obj in dest.lower():
            include = False
            print("File excluded:", dest)
            break
    if include:
        to_keep.append((dest, source, kind))
a.binaries = to_keep
to_keep = []
for (dest, source, kind) in a.datas:
    include = True
    for obj in to_exclude:
        if obj in dest.lower():
            include = False
            print("File excluded:", dest)
            break
    if include:
        to_keep.append((dest, source, kind))
a.datas = to_keep
print("****************************************")
print(a.binaries)
print(a.datas)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Diary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['style\\logo.png'],
)
