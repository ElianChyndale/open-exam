# Start ExamOS Web frontend
param(
    [int]$Port = 3000
)

Set-Location "$PSScriptRoot\apps\web"

if (-not $env:NEXT_PUBLIC_API_URL) {
    $env:NEXT_PUBLIC_API_URL = "http://localhost:8000"
}

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting ExamOS Web on http://localhost:$Port" -ForegroundColor Cyan
Write-Host "API URL: $env:NEXT_PUBLIC_API_URL" -ForegroundColor DarkGray

& ".\node_modules\.bin\next.cmd" dev -p $Port
