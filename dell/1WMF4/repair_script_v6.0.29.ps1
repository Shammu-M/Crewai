

write-output "Start .NET Desktop Runtime repair routine." | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append
$repair = $false
$installedSW = Get-ChildItem "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
foreach($obj in $installedSW){

    $name = $obj.GetValue('DisplayName')
    if ($null -ne $name){
        if ($name -like "*Microsoft Windows Desktop Runtime*"){
            write-output $obj.GetValue('DisplayName') | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append
            if ($name -like "*6.0.29*"){
                write-output "Latest .NET Desktop Runtime version 6.0.29 installed." | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append
            }
            else{
                # Detected older minor version of .NET Desktop Runtime is installed, repair operation required.
                # e.g. v6.022 and v6.0.18 are installed
                $repair = $true
            }

        }
    }
}

if ($repair){
    write-output ".NET Desktop Runtime repair is required." | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append
    $cmd = 'c:\DELL\1WMF4\windowsdesktop-runtime-6.0.29-win-x64.exe'
    $parms = "/repair /passive /norestart /log c:\windows\logs\dotnet6.0.29_repair.log" 
    $parms = $parms.Split(" ")
    write-output "Begin repair operation." | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append
    Start-Process -FilePath $cmd -ArgumentList $parms -Wait
    write-output "Repair operation complete." | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append

}
else{

    write-output "Older versions of .NET Desktop Runtime are not installed, repair operation not required. " | Out-File -FilePath c:\windows\logs\dotnet_versions.log -append

}      

  
