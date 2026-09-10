$HKCUsftw =  'HKCU:SOFTWARE\Classes\Local Settings\Software'
$HKCUsftwMS =  'HKCU:SOFTWARE\Classes\Local Settings\Software\Microsoft'
$HKCUsftwMSwindows =  'HKCU:SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows'
$HKCUsftwMSwindowsCV =  'HKCU:SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion'
$HKCUsftwMSwindowsCVam =  'HKCU:SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel'
$HKCUsftwMSwindowsCVamRepo =  'HKCU:SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository'
$SystemAccount = New-Object System.Security.Principal.NTAccount("NT AUTHORITY\SYSTEM")

$HKCUsftwExists =  Test-Path $HKCUsftw
$HKCUsftwMSExists =  Test-Path $HKCUsftwMS
$HKCUsftwMSwindowsExists =  Test-Path $HKCUsftwMSwindows
$HKCUsftwMSwindowsCVExists =  Test-Path $HKCUsftwMSwindowsCV
$HKCUsftwMSwindowsCVamExists =  Test-Path $HKCUsftwMSwindowsCVam
$HKCUsftwMSwindowsCVamRepoExists =  Test-Path $HKCUsftwMSwindowsCVamRepo


if (!$HKCUsftwExists)
{
    New-Item -Path $HKCUsftw
    Write-Output "Reg path created - $($HKCUsftw)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}

if (!$HKCUsftwMSExists)
{
    New-Item -Path $HKCUsftwMS
    Write-Output "Reg path created - $($HKCUsftwMS)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}

if (!$HKCUsftwMSwindowsExists)
{
    New-Item -Path $HKCUsftwMSwindows
    Write-Output "Reg path created - $($HKCUsftwMSwindows)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}

if (!$HKCUsftwMSwindowsCVExists)
{
    New-Item -Path $HKCUsftwMSwindowsCV
    Write-Output "Reg path created - $($HKCUsftwMSwindowsCV)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}

if (!$HKCUsftwMSwindowsCVamExists)
{
    New-Item -Path $HKCUsftwMSwindowsCVam
    Write-Output "Reg path created - $($HKCUsftwMSwindowsCVam)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}

if (!$HKCUsftwMSwindowsCVamRepoExists)
{
    New-Item -Path $HKCUsftwMSwindowsCVamRepo
    Write-Output "Reg path created - $($HKCUsftwMSwindowsCVamRepo)" | Tee-Object -FilePath C:\Windows\Logs\HKCUregistry.log -Append
}


<#
#Setting Ownership to SYSTEM is not working via powershell
#Ownership set by loading a hive that has ownership already set to SYSTEM

$Acl = Get-Acl -Path $HKCUsftwMSwindowsCVamRepo

$Acl.SetOwner($SystemAccount)

Set-Acl -Path $HKCUsftwMSwindowsCVamRepo -AclObject $Acl


$Acl = Get-Acl -Path $HKCUsftwMSwindowsCVam

$Acl.SetOwner($SystemAccount)

Set-Acl -Path $HKCUsftwMSwindowsCVam -AclObject $Acl

#>
