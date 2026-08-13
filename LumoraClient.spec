# -*- mode: python ; coding: utf-8 -*-

import os

from PyInstaller.utils.hooks import collect_all


numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all(
    "numpy"
)

mt5_datas, mt5_binaries, mt5_hiddenimports = collect_all(
    "MetaTrader5"
)


a = Analysis(
    ["client/main.py"],

    pathex=[
        os.path.abspath("."),
    ],

    binaries=(
        numpy_binaries
        + mt5_binaries
    ),

    datas=(
        numpy_datas
        + mt5_datas
    ),

    hiddenimports=(
        numpy_hiddenimports
        + mt5_hiddenimports
    ),

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],

    noarchive=False,
    optimize=0,
)


pyz = PYZ(
    a.pure
)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],

    name="LumoraClient",

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
)