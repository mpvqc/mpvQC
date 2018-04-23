# -*- mode: python -*-

block_cipher = None


a = Analysis(['tmpv.py'],
             pathex=['/home/elias/PycharmProjects/mpvQC'],
             binaries=[
                ('/home/elias/PycharmProjects/mpvQC/locale/de/LC_MESSAGES/*.*', 'locale/de/LC_MESSAGES'),
                ('/home/elias/PycharmProjects/mpvQC/locale/en/LC_MESSAGES/*.*', 'locale/en/LC_MESSAGES')
             ],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='tmpv-executable',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
