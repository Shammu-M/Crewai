# Remove all Intel PPM packages


$obj = get-provisioningpackage
Write-Output $obj.Count


foreach ($ppmpkg in $obj)
{
	Write-Output $ppmpkg.PackageName
    if ($ppmpkg.PackageName -eq "Intel.Power.Settings.Processor") {
		Uninstall-ProvisioningPackage -PackageId $ppmpkg.PackageId
    }
}

exit 0