Import-Module $PSScriptRoot/powershell/utils.psm1

python ./versioning.py

./activate.ps1
python ./src/main.py