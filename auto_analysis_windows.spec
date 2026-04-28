# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


ROOT = Path.cwd()

datas = [
    (str(ROOT / "templates"), "templates"),
    (str(ROOT / "static"), "static"),
    (str(ROOT / "design-system"), "design-system"),
    (str(ROOT / "classification_units.json"), "."),
    (str(ROOT / "geo_cut_model.json"), "."),
    (str(ROOT / "ebsi_geo_data.json"), "."),
]

sample_archives = ROOT / "samples" / "archives"
local_archives = ROOT / "archives"
if sample_archives.exists():
    datas.append((str(sample_archives), "archives"))
elif local_archives.exists():
    datas.append((str(local_archives), "archives"))


a = Analysis(
    ["auto_analysis_launcher.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Auto Analysis",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Auto Analysis",
)
