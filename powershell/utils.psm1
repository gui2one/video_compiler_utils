function Print([string]$message) {
    Write-Host "-----------------------------"
    Write-Host "$message"
    Write-Host "-----------------------------"
}

Export-ModuleMember -Function Print


function CreateFolder([string]$folder_path){
    if( Test-Path -Path $folder_path -PathType Container){
        Print('Folder exists')
    }else{
        New-Item $folder_path -ItemType Directory
    }
}
Export-ModuleMember -Function CreateFolder
function RemoveFolderIfExists([string]$folder_path){
    if( Test-Path -Path $folder_path -PathType Container){
        Remove-Item $folder_path -Recurse -Force
        Write-Host "[build script] Successfully Remove Directory: $folder_path"
    }else{
        Write-Host "[build script] Directory not found : $folder_path"
    }
}

Export-ModuleMember -Function RemoveFolderIfExists

function RemoveFileIfExists([string]$file_path){
    if( Test-Path -Path $file_path -PathType Leaf){
        Remove-Item $file_path -Force
    }else{
        Write-Host "[build script] File not found : $file_path"
    }
}

Export-ModuleMember -Function RemoveFileIfExists