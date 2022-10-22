Import-Module $PSScriptRoot/powershell/utils.psm1

CreateFolder("./dist/src/")
pyinstaller --onefile --noconfirm --noconsole --paths=$PSScriptRoot\env\Lib\site-packages ./src/main.py
try {
    
    Copy-Item ./src/style.qss ./dist/src/
    Remove-Item ./dist/VCU.exe 
    Rename-Item ./dist/main.exe VCU.exe

    Invoke-Expression ./dist/VCU.exe
}
catch {}
 