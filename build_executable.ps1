$exe = "vcu.exe"
$icon = "VCU_logo_01.ico"
Import-Module $PSScriptRoot/powershell/utils.psm1
$ffmpeg_local_dir = "C:/gui2one/ffmpeg"
pyinstaller --onedir `
    --noconfirm `
    --noconsole `
    --icon=VCU_logo_01.ico `
    --paths=$PSScriptRoot\env\Lib\site-packages `
    ./src/main.py
CreateFolder("./dist/main/src/")
CreateFolder("./dist/main/3rd-party/")
try {
    
    Copy-Item $ffmpeg_local_dir -Recurse ./dist/main/3rd-party/
    Copy-Item ./src/style.qss ./dist/main/src/
    Copy-Item ./src/$icon ./dist/main/src/
    Rename-Item ./dist/main/main.exe $exe

    Invoke-Expression ./dist/main/$exe
}
catch {}
 