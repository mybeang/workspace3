# -*- mode: python -*-

block_cipher = None


a = Analysis(['one_file_raw.py'],
             pathex=['D:\\python_project\\workspace3\\socket_program',
             "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.17763.0\\ucrt\\DLLs\\x86"],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='one_file_raw',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
