# -*- mode: python ; coding: utf-8 -*-

import os

from PyInstaller.utils.hooks import collect_dynamic_libs


# ==========================================================
# PYSIDE6
# ==========================================================

pyside6_binaries = collect_dynamic_libs(
    "PySide6"
)


# ==========================================================
# METATRADER5
# ==========================================================

mt5_binaries = collect_dynamic_libs(
    "MetaTrader5"
)


# ==========================================================
# ANALYSIS
# ==========================================================

a = Analysis(
    ["client/main.py"],

    pathex=[
        os.path.abspath("."),
    ],

    binaries=(
        pyside6_binaries
        + mt5_binaries
    ),

    datas=[],

    hiddenimports=[
        "MetaTrader5",
        "MetaTrader5._core",
        "numpy",
        "numpy._core",
        "numpy._core._multiarray_umath",
    ],

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[
        "numpy.tests",
        "numpy.testing",
        "numpy._core._multiarray_tests",
        "numpy._core._operand_flag_tests",
        "numpy._core._rational_tests",
        "numpy._core._struct_ufunc_tests",
        "numpy._core._umath_tests",
    ],

    noarchive=False,

    optimize=0,
)


# ==========================================================
# PYZ
# ==========================================================

pyz = PYZ(
    a.pure
)


# ==========================================================
# EXE
# ==========================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],

    name="LumoraClient",

    icon="LumoraIcon.ico",

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