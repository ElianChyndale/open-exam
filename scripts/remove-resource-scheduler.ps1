param(
    [string]$TaskName = "OpenExam-ResourceOS"
)

$ErrorActionPreference = "Stop"
schtasks.exe /Delete /TN $TaskName /F
if ($LASTEXITCODE -ne 0) {
    throw "Failed to remove scheduled task '$TaskName'."
}

Write-Host "Removed '$TaskName'."
