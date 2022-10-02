pyinstaller --onefile --noconfirm --noconsole --paths=$PSScriptRoot\env\Lib\site-packages ./src/main.py

mkdir ./dist/src/
Copy-Item ./src/style.qss ./dist/src/

Rename-Item ./dist/main.exe VCU.exe 