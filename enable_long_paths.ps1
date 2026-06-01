# Script to enable Windows Long Path support
# This script must be run as Administrator

Write-Host "Enabling Windows Long Path support..." -ForegroundColor Yellow
Write-Host "This requires Administrator privileges." -ForegroundColor Yellow

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    exit 1
}

# Enable Long Paths via Registry
$registryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem"
$propertyName = "LongPathsEnabled"
$propertyValue = 1

try {
    $currentValue = Get-ItemProperty -Path $registryPath -Name $propertyName -ErrorAction SilentlyContinue
    
    if ($currentValue -and $currentValue.$propertyName -eq 1) {
        Write-Host "Long Path support is already enabled!" -ForegroundColor Green
    } else {
        Set-ItemProperty -Path $registryPath -Name $propertyName -Value $propertyValue -Type DWord
        Write-Host "Long Path support has been enabled successfully!" -ForegroundColor Green
        Write-Host "You may need to restart your computer for the changes to take full effect." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error: Failed to modify registry. $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "After enabling (and restarting if needed), you can install TensorFlow with:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "  python -m pip install tensorflow-cpu" -ForegroundColor Cyan




