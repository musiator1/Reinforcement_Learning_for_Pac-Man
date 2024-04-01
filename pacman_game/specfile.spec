# specfile.spec

block_cipher = None

a = Analysis([r'C:\Users\rafal\Desktop\STUDIA\SEM4\Projekt indywidualny\Reinforcement_Learning_for_Pac-Man\pacman_game\src\game_main.py'],
             pathex=[r'C:\Users\rafal\Desktop\STUDIA\SEM4\Projekt indywidualny\Reinforcement_Learning_for_Pac-Man\pacman_game'], # Tutaj podaj ścieżkę do katalogu głównego projektu
             binaries=[],
             datas=[(r'C:\Users\rafal\Desktop\STUDIA\SEM4\Projekt indywidualny\Reinforcement_Learning_for_Pac-Man\pacman_game\resources\*', r'pacman_game\resources')], # Jeśli używasz obrazów lub innych plików, które aplikacja ma wykorzystywać, dodaj je tutaj
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
          name='Pac-Man', # Tutaj podaj nazwę, jaką ma mieć plik wykonywalny
          debug=False,
          strip=False,
          upx=True,
          console=False)
