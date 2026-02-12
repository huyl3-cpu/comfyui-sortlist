@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo   Rename all images to 1.png, 2.png, 3.png...
echo ============================================
echo.

REM Check if ffmpeg is available (for conversion)
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: ffmpeg not found in PATH!
    echo Please install ffmpeg or add it to PATH.
    pause
    exit /b 1
)

REM Counter
set counter=1

REM Process all image files
for %%f in (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.tif) do (
    if exist "%%f" (
        echo [!counter!] Converting: %%f -^> !counter!.png
        
        REM Convert to PNG using ffmpeg
        ffmpeg -i "%%f" -y "!counter!.png" >nul 2>&1
        
        if !errorlevel! equ 0 (
            REM Delete original if different from output
            if /i not "%%f"=="!counter!.png" (
                del "%%f"
            )
        ) else (
            echo    ERROR: Failed to convert %%f
        )
        
        set /a counter+=1
    )
)

set /a total=counter-1
echo.
echo ============================================
echo   Done! Renamed %total% images.
echo ============================================
pause
