function Print([string]$message) {
    Write-Host "$message ... fucker !!!"
}

Export-ModuleMember -Function Print

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