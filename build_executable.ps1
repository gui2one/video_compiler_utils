pyinstaller --onefile --noconfirm --noconsole --paths=$PSScriptRoot\env\Lib\site-packages ./src/main.py
try {
    
    mkdir ./dist/src/
    Copy-Item ./src/style.qss ./dist/src/
    Remove-Item ./dist/VCU.exe 
    Rename-Item ./dist/main.exe VCU.exe
}
catch {}
 