$app_name = "vcu"

$exe = "$app_name.exe"
$icon = "VCU_logo_01.ico"
$dist_dir = "./dist/$app_name"
Import-Module $PSScriptRoot/powershell/utils.psm1

python ./versioning.py

$ffmpeg_local_dir = "C:/gui2one/ffmpeg"
pyinstaller --onedir `
    --noconfirm `
    --noconsole `
    --icon=VCU_logo_01.ico `
    --name "$app_name" `
    --paths=$PSScriptRoot\env\Lib\site-packages `
    ./src/main.py
CreateFolder("$dist_dir/src/")
CreateFolder("$dist_dir/3rd-party/")
try {
    # temporary -- DO NOT leaves this in distribution !
    Copy-Item ./database.db $dist_dir
    ###################

    Copy-Item $ffmpeg_local_dir -Recurse $dist_dir/3rd-party/
    Copy-Item ./src/style.qss $dist_dir/src/
    Copy-Item ./src/$icon $dist_dir/src/
    Copy-Item ./src/icons -Recurse $dist_dir/src/ 


    Invoke-Expression $dist_dir/$exe
}
catch {}
 