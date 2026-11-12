# ==============================================================================
# BioDINO-Edge: Multi-ABI Automated Release Build Script
# ==============================================================================
# Builds standalone, production-ready APKs for each CPU architecture:
#   1. arm64-v8a  -> Modern 64-bit phones (99% of Android devices)
#   2. armeabi-v7a -> Legacy 32-bit Android phones
#   3. universal   -> Fat APK containing native binaries for all architectures
#
# Output artifacts and SHA256 checksums are gathered into:
#   android_app/release_outputs/
# ==============================================================================

param(
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$OutputDir = Join-Path $ScriptDir "release_outputs"
if (Test-Path $OutputDir) {
    Remove-Item -Recurse -Force $OutputDir
}
New-Item -ItemType Directory -Path $OutputDir | Out-Null

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " BioDINO-Edge: Multi-ABI Automated Release Build (v$Version)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$SourceApk = Join-Path $ScriptDir "app\build\outputs\apk\release\app-release.apk"

# 1. Build arm64-v8a (Primary high-efficiency edge binary)
Write-Host "`n[1/3] Building arm64-v8a release APK..." -ForegroundColor Cyan
.\gradlew.bat assembleRelease -PtargetAbi=arm64-v8a --no-daemon
if (-not (Test-Path $SourceApk)) {
    Write-Error "Failed to locate generated arm64-v8a APK at $SourceApk"
}
$Arm64Dest = Join-Path $OutputDir "BioDINO-Edge-v$Version-arm64-v8a.apk"
Move-Item -Path $SourceApk -Destination $Arm64Dest -Force
$Arm64Size = [math]::Round(((Get-Item $Arm64Dest).Length / 1MB), 2)
Write-Host "  -> Generated: BioDINO-Edge-v$Version-arm64-v8a.apk ($Arm64Size MB)" -ForegroundColor Green

# 2. Build armeabi-v7a (Legacy 32-bit fallback)
Write-Host "`n[2/3] Building armeabi-v7a release APK..." -ForegroundColor Cyan
.\gradlew.bat assembleRelease -PtargetAbi=armeabi-v7a --no-daemon
if (-not (Test-Path $SourceApk)) {
    Write-Error "Failed to locate generated armeabi-v7a APK at $SourceApk"
}
$ArmV7Dest = Join-Path $OutputDir "BioDINO-Edge-v$Version-armeabi-v7a.apk"
Move-Item -Path $SourceApk -Destination $ArmV7Dest -Force
$ArmV7Size = [math]::Round(((Get-Item $ArmV7Dest).Length / 1MB), 2)
Write-Host "  -> Generated: BioDINO-Edge-v$Version-armeabi-v7a.apk ($ArmV7Size MB)" -ForegroundColor Green

# 3. Build Universal Multi-Arch APK
Write-Host "`n[3/3] Building Universal multi-arch release APK..." -ForegroundColor Cyan
.\gradlew.bat assembleRelease -PallAbis --no-daemon
if (-not (Test-Path $SourceApk)) {
    Write-Error "Failed to locate generated Universal APK at $SourceApk"
}
$UnivDest = Join-Path $OutputDir "BioDINO-Edge-v$Version-universal.apk"
Move-Item -Path $SourceApk -Destination $UnivDest -Force
$UnivSize = [math]::Round(((Get-Item $UnivDest).Length / 1MB), 2)
Write-Host "  -> Generated: BioDINO-Edge-v$Version-universal.apk ($UnivSize MB)" -ForegroundColor Green

# 4. Copy Tier-2 Companion Model asset for GitHub Release
$RootCompanion = Join-Path $ScriptDir "..\biodino_companion_int8.onnx"
if (Test-Path $RootCompanion) {
    $CompanionDest = Join-Path $OutputDir "biodino_companion_int8.onnx"
    Copy-Item -Path $RootCompanion -Destination $CompanionDest -Force
    $CompSize = [math]::Round(((Get-Item $CompanionDest).Length / 1MB), 2)
    Write-Host "`n[4/4] Copied Tier-2 Companion Model: biodino_companion_int8.onnx ($CompSize MB)" -ForegroundColor Magenta
}

# 5. Generate SHA256 Checksums
Write-Host "`n[5/5] Generating SHA256 Checksums manifest..." -ForegroundColor Cyan
$ChecksumFile = Join-Path $OutputDir "checksums_sha256.txt"
$Artifacts = Get-ChildItem -Path $OutputDir -File | Where-Object { $_.Name -ne "checksums_sha256.txt" }
$ChecksumLines = @()
foreach ($item in $Artifacts) {
    $hash = (Get-FileHash -Path $item.FullName -Algorithm SHA256).Hash.ToLower()
    $ChecksumLines += "$hash  $($item.Name)"
}
$ChecksumLines | Out-File -FilePath $ChecksumFile -Encoding utf8
Write-Host "  -> Generated: checksums_sha256.txt" -ForegroundColor Green

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " All Release Binaries Built Successfully!" -ForegroundColor Green
Write-Host " Output directory: $OutputDir" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
Get-ChildItem -Path $OutputDir | Select-Object Name, Length | Format-Table -AutoSize
