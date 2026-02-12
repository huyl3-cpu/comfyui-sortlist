@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo   Rename all videos to 1.mp4, 2.mp4, 3.mp4...
echo ============================================
echo.

REM Check if ffmpeg is available
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: ffmpeg not found in PATH!
    echo Please install ffmpeg or add it to PATH.
    pause
    exit /b 1
)

REM Counter
set counter=1

REM Process all video files
for %%f in (*.mp4 *.avi *.mkv *.mov *.flv *.webm *.wmv *.m4v *.mpg *.mpeg) do (
    if exist "%%f" (
        echo [!counter!] Converting: %%f -^> !counter!.mp4
        
        REM Convert to MP4 using ffmpeg (fast copy if possible)
        ffmpeg -i "%%f" -c copy -y "!counter!.mp4" >nul 2>&1
        
        if !errorlevel! neq 0 (
            REM If copy fails, re-encode
            echo    Copy failed, re-encoding...
            ffmpeg -i "%%f" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -y "!counter!.mp4" >nul 2>&1
        )
        
        if !errorlevel! equ 0 (
            REM Delete original if different from output
            if /i not "%%f"=="!counter!.mp4" (
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
echo   Done! Renamed %total% videos.
echo ============================================
pause
