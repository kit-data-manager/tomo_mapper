# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all Magika-related files
magika_datas, magika_binaries, magika_hiddenimports = collect_all('magika')

a = Analysis(
    ['mapping_cli.py'],
    pathex=[],
    binaries=magika_binaries,
    datas=[
        ('src/resources', 'src/resources'),
        *magika_datas,  # Include Magika's data files
    ],
    hiddenimports=magika_hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='sem_tomo_mapper',
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
)