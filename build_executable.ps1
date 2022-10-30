Import-Module $PSScriptRoot/powershell/utils.psm1
$ffmpeg_local_dir = "C:/gui2one/ffmpeg"
pyinstaller --onedir --noconfirm --paths=$PSScriptRoot\env\Lib\site-packages ./src/main.py
CreateFolder("./dist/main/src/")
CreateFolder("./dist/main/3rd-party/")
try {
    
    Copy-Item $ffmpeg_local_dir -Recurse ./dist/main/3rd-party/
    Copy-Item ./src/style.qss ./dist/main/src/
    Remove-Item ./dist/main/VCU.exe 
    Rename-Item ./dist/main/main.exe VCU.exe

    Invoke-Expression ./dist/main/VCU.exe
}
catch {}
 