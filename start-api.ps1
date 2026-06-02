# Start ExamOS API server
param(
    [int]$Port = 8000,
    [switch]$Reload = $false
)

$Root = $PSScriptRoot
$Packages = @(
    "$Root\.system",
    "$Root\apps\api",
    "$Root\packages\exam-core\src",
    "$Root\packages\study-science\src",
    "$Root\packages\agent-runtime\src",
    "$Root\packages\learning-records\src",
    "$Root\packages\learner-twin\src",
    "$Root\packages\language-science\src",
    "$Root\packages\resource-ingestion\src"
)
$env:PYTHONPATH = ($Packages -join ";")

Write-Host "Starting ExamOS API on http://localhost:$Port" -ForegroundColor Cyan
Write-Host "PYTHONPATH: $env:PYTHONPATH" -ForegroundColor DarkGray

if ($Reload) {
    python -m uvicorn main:app --app-dir "$Root\apps\api" --host 0.0.0.0 --port $Port --reload
} else {
    python -m uvicorn main:app --app-dir "$Root\apps\api" --host 0.0.0.0 --port $Port --workers 2
}
