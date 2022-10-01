pyinstaller --onedir --noconfirm --noconsole --paths=$PSScriptRoot\env\Lib\site-packages ./src/main.py

mkdir ./dist/main/src/
Copy-Item ./src/style.qss ./dist/main/src/