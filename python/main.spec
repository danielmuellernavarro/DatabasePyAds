# -*- mode: python -*-
a = Analysis(['main.py'],
             hiddenimports=['pkg_resources'],
             hookspath=None,
             runtime_hooks=None)
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyads.exe',
          debug=False,
          strip=None,
          upx=False,
          console=True
)