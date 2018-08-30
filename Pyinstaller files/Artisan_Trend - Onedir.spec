# -*- mode: python -*-

block_cipher = None


a = Analysis(['Artisan_Trend.py'],
             pathex=['C:\\Users\\Riley\\Documents\\work\\Artisan-Trend-master'],
             binaries=[('C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/x86', '.' )],#, ('C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/x64', '.' ), ('C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/x86', '.' )],
             datas=[('C:/Users/Riley/AppData/Local/Programs/Python/Python36-32/Lib/site-packages/plotly/', './plotly/')],
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
          exclude_binaries=True,
          name='Artisan Trend',
          icon = 'artisan_logo.ico',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries+[('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
              ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')],
               a.zipfiles,
               a.datas+ [('artisan_logo.ico', 'C:/Users/Riley/Documents/work/Artisan-Trend-master/artisan_logo.ico',  'DATA')],
               strip=False,
               upx=True,
               name='Artisan Trend')
