# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file to create macOS bundle. Windows bundle is currently broken, see:
# https://github.com/pyinstaller/pyinstaller/issues/3020
block_cipher = None

add_resources = [
    ('resources/light/*', 'themes/light/'),
    ('resources/dark/*', 'themes/dark/'),
    ('libqnotero/ui/*', 'libqnotero/ui/'),
]

add_imports = [
    "libqnotero.qnoteroQuery",
    "libqnotero.qnoteroResults",
    "libqnotero._themes.light",
    "libqnotero._themes.dark",
    "libqnotero._themes.",
]

add_pathexes =['./libqnotero',
                     './libzotero',
                     './qnotero',
                     './libqnotero/qt',
               ]

a = Analysis(['qnotero'],
             pathex=add_pathexes,
             binaries=[],
             datas=add_resources,
             hiddenimports=add_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='qnotero',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='qnotero'
               )
app = BUNDLE(coll,
             name='Qnotero.app',
             icon='./resources/qnotero.icns',
             bundle_identifier='edu.ipn.esiqie.qnotero',
             info_plist={
                 'NSHighResolutionCapable': 'True',
                 'LSUIElement': 1
             }
             )
