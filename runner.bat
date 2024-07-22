@echo off
setlocal enabledelayedexpansion

set ASSETSDIR=assets
set ASSETS=%ASSETSDIR%\minecraft\
set PATCH=patch\minecraft\
set OUTPUT=OUTPUT\3dscraft\resourcepacks\minecraft\

if "%1"=="" (
    echo Using default ASSETS path: %ASSETSDIR%
) else (
    set ASSETS=%1\minecraft\
    echo Using provided ASSETS path: %ASSETSDIR%
)

if not exist "%ASSETS%" (
    echo Error: ASSETS directory does not exist: %ASSETS%
    exit /b 1
)

if not exist "%PATCH%" (
    echo Error: PATCH directory does not exist: %PATCH%
    exit /b 1
)

if not exist "%OUTPUT%" (
    echo Creating OUTPUT directory: output\
    mkdir output\
    mkdir "%OUTPUT%"
)

for /f "usebackq tokens=* delims=" %%f in ("files.txt") do (
    if not "%%f"=="" (
        set "line=%%f"
        echo !line! | findstr /c:"#">nul
        if !errorlevel! == 1 (
            set "src=%ASSETS%%%f"
            set "dest=%OUTPUT%%%f"
            
            if not exist "!src!" (
                echo File not found, aborting: !src!
                echo Make sure file is in place, and has right name.
                echo Also make sure you are using files.txt for your provided assets version.
                exit /b 1
            )

            for %%d in ("!dest!") do if not exist "%%~dpd" mkdir "%%~dpd"
            
            echo Copying !src!
            copy /y "!src!" "!dest!" > NUL
        )
    )
)

echo Copying all files from PATCH to OUTPUT..
xcopy /e /i /y "%PATCH%" "%OUTPUT%" > NUL

echo Operation completed.
echo  -
echo    Place the contents inside of the new "OUTPUT" directory in the root of your sd card, then you may start playing 3DSCraft.
echo    - ChatGPT and Team Omega.
echo  -
echo    For Copyright reasons, you are strictly forbidden sharing this around in any way, it is for your use only, through your legal act of buying minecraft and getting the assets.
echo  -
echo  - 3DSCraft ResourcePacker done.
pause
