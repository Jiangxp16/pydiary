# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['core\\start.py'],
    pathex=[],
    binaries=[],
    datas=[('style\\*', '.\\style')],
    hiddenimports=['holidays.countries'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PySide6.qml",
        "PySide6.resources",
        "Pillow",
    ],
    noarchive=False,
)
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['style\\logo.png'],
)
