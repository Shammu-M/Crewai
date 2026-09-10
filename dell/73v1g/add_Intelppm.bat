@echo off
rem =======================================================================================
rem USAGE:
rem for DUP: add_intelppm.bat
rem for FI: add_intelppm.bat <ppm_file_dir>\ . Example: add_intelppm.bat c:\dell\4R6RN\
rem ========================================================================================

set myReturnCode=0
set myReturnCodeName=SUCCESS

:CHECK_OS
rem myOS: WIN10, WIN11_SV1, WIN11_SV2

for /f "tokens=4-7 delims=[.] " %%i in ('ver') do (if %%i==Version (
        rem set OSVer=%%j.%%k.%%l.%%m
        set WinMajorBuild=%%l
        set WinMinorBuild=%%m
    ) else (
	    rem set OSVer=%%i.%%j.%%k.%%l
		set WinMajorBuild=%%k
        set WinMinorBuild=%%l
	)
)

echo Windows Version = %WinMajorBuild%.%WinMinorBuild%

if %WinMajorBuild% geq 22621 (
    set myOS=WIN11_SV2
) else if %WinMajorBuild% leq 19045 (
    set myOS=WIN10
) else (
    set myOS="WIN11_SV1"
)

echo myOS = %myOS%


:CHECK_CPU
rem myCPU: SPR, LNL, MTL, RPL, ADL-N, ADL, TGL, 0 (No supported CPU)

set myCPU=0

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 143") && (set myCPU=SPR) && (goto FILEPATH)

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 189") && (set myCPU=LNL) && (goto FILEPATH)

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 170") && (set myCPU=MTL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 172") && (set myCPU=MTL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 181") && (set myCPU=MTL) && (goto FILEPATH)

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 183") && (set myCPU=RPL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 186") && (set myCPU=RPL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 191") && (set myCPU=RPL) && (goto FILEPATH)

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 151") && (set myCPU=ADL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 154") && (set myCPU=ADL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 190") && (set myCPU=ADL-N) && (goto FILEPATH)

(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 140") && (set myCPU=TGL) && (goto FILEPATH)
(echo %PROCESSOR_IDENTIFIER%| find "Family 6 Model 141") && (set myCPU=TGL) && (goto FILEPATH)

rem return 20 for DUP (ERROR_INSTALL_PLATFORM_UNSUPPORTED) (DU not support non-zero ReturnCode yet)
rem set myReturnCode=20
set myReturnCodeName=ERROR_INSTALL_PLATFORM_UNSUPPORTED

goto END


:FILEPATH
echo myCPU = %myCPU%

set myFile=PPM-Win10-preview-v1000.20221101.ppkg

if "%myCPU%"=="SPR" (
 	if "%myOS%"=="WIN11_SV2" (
	    set myFile=PPM-SPR-preview-v2000.20231027.ppkg
    ) else (
	    rem Win11 SV1 and Win10
	    set myFile=inbox
	)
    goto INSTALL
)

if "%myCPU%"=="LNL" (
 	if "%myOS%"=="WIN11_SV2" (
	    set myFile=PPM-LNL-preview-v1006.20230906.ppkg
    ) else (
	    rem Win11 SV1 and Win10
	    set myFile=inbox
	)
    goto INSTALL
)

if "%myCPU%"=="MTL" (
 	if "%myOS%"=="WIN11_SV2" (
	    set myFile=PPM-MTL-preview-v1004.20231025.ppkg
    ) else (
	    rem Win11 SV1 and Win10
	    set myFile=PPM-Win10-MTL-preview-v1000.20230905.ppkg
	)
    goto INSTALL
)

if "%myCPU%"=="RPL" (
 	if "%myOS%"=="WIN11_SV2" (
	    set myFile=PPM-RPL-preview-v1003.20230524.ppkg
    )
    goto INSTALL
)

if "%myCPU%"=="ADL-N" (
 	if "%myOS%"=="WIN10" (
	    rem Win10
	    set myFile=PPM-ADL-N-preview-v1000.20220719.ppkg
    ) else (
	    rem Win11
	    set myFile=PPM-ADL-N-preview-v1001.20220811.ppkg
	)
	
    goto INSTALL
)

if "%myCPU%"=="ADL" (
 	if "%myOS%"=="WIN11_SV1" (
	    set myFile=PPM-ADL-preview-v1001.20220331.ppkg
    ) else if "%myOS%"=="WIN11_SV2" (
	    rem Win11 SV2 (inbox)
	    set myFile=inbox
	)
	
    goto INSTALL
)

if "%myCPU%"=="TGL" (
    set myFile=PPM-TGL-preview-v9.402.ppkg

    goto INSTALL
)

:INSTALL

if [%1] == [] (
	set myPPMPath="%~dp0%myFile%"
	set myPs1Path="%~dp0del_Intelppm.ps1"
)else (
	set myPPMPath="%1%myFile%"
	set myPs1Path="%1del_Intelppm.ps1"
)

rem echo myPPMPath = %myPPMPath%
rem echo myPs1Path = %myPs1Path%

rem Uninstall old PPM
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%myPs1Path%'";

rem Install PPM
if exist %myPPMPath% (
    echo PPM file = %myFile%
    provtool %myPPMPath% /quiet
)

if not %ERRORLEVEL% == 0 (
	exit 1
)


:END

rem
rem Set Registry for Inventory
rem

set PPM_KEY="HKLM\SOFTWARE\Dell\ManageableUpdatePackage\IntelPPM"
set PPM_NAME="Intel Common PPM Package"
set PPM_VERSION=2.1.1

reg add %PPM_KEY% /f
reg add %PPM_KEY% /v Product_Name /t REG_SZ /d %PPM_NAME% /f
reg add %PPM_KEY% /v Product_Version /t REG_SZ /d %PPM_VERSION% /f
reg add %PPM_KEY% /v ReturnCode_Name /t REG_SZ /d %myReturnCodeName% /f



exit myReturnCode




