param(
    [string]$TaskName = "OpenExam-ResourceOS"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$ResourceScript = Join-Path $RepoRoot "scripts\resources.py"
$Python = (Get-Command python -ErrorAction Stop).Source
$TaskCommand = "`"$Python`" `"$ResourceScript`" run-due --scheduled"

schtasks.exe /Create /TN $TaskName /SC HOURLY /MO 6 /TR $TaskCommand /F
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install scheduled task '$TaskName'."
}

Write-Host "Installed '$TaskName'. It will run ResourceOS subscriptions every 6 hours."
