# Start ExamOS API server
param(
    [int]$Port = 8000,
    [switch]$Reload = $false
)

$env:PYTHONPATH = "$PSScriptRoot\.system;$PSScriptRoot\apps\api;$PSScriptRoot\packages\exam-core\src;$PSScriptRoot\packages\study-science\src;$PSScriptRoot\packages\agent-runtime\src"

Write-Host "Starting ExamOS API on http://localhost:$Port" -ForegroundColor Cyan
Write-Host "PYTHONPATH: $env:PYTHONPATH" -ForegroundColor DarkGray

if ($Reload) {
    python -m uvicorn main:app --app-dir "$PSScriptRoot\apps\api" --host 0.0.0.0 --port $Port --reload
} else {
    python -m uvicorn main:app --app-dir "$PSScriptRoot\apps\api" --host 0.0.0.0 --port $Port --workers 2
}
