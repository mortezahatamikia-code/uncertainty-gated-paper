@echo off
setlocal
cd /d "%~dp0"
echo ==============================================================
echo  BioDINO-Edge: Multi-ABI Automated Release Build
echo ==============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_release_apks.ps1"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] All APKs built and packaged into android_app\release_outputs\
) else (
    echo.
    echo [ERROR] Build failed with exit code %ERRORLEVEL%
)
pause

