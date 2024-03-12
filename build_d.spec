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
    exclude_binaries=True,
    # contents_directory='.', # default to _internal
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
"""
a2 = Analysis(
    ['core\\xxxxx.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
exe2 = EXE(
    PYZ(a2.pure),
    a2.scripts,
    exclude_binaries=True,
    # contents_directory='.', # default to _internal
    name='xxx',
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
"""
exes = [
    exe,
    # exe2,
]

coll = COLLECT(*exes,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Diary',   # name of directory
               )
