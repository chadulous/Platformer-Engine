python -m PyInstaller --noconfirm --onedir --windowed --name "Maria" --add-data "maps;maps/" --add-data "BAHNSCHRIFT.TTF;."  "main.py"
Compress-Archive "dist/Maria" "dist.zip"