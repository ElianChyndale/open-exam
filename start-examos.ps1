# Start ExamOS: API + Web + dependency check, one command.
param(
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000,
    [switch]$NoBrowser,
    [switch]$SkipDeps
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$ApiUrl = "http://127.0.0.1:$ApiPort"
$WebUrl = "http://127.0.0.1:$WebPort"

# Ensure log directory exists
$null = New-Item -Path "$Root\.system\logs" -ItemType Directory -Force

# ── Helpers ──

function Write-Info  { Write-Host "INFO  $($args -join ' ')" -ForegroundColor Cyan }
function Write-Ok    { Write-Host "OK    $($args -join ' ')" -ForegroundColor Green }
function Write-Warn  { Write-Host "WARN  $($args -join ' ')" -ForegroundColor Yellow }
function Write-Err   { Write-Host "ERROR $($args -join ' ')" -ForegroundColor Red }

function Wait-ForUrl {
    param([string]$Url, [string]$Name, [int]$Seconds = 90)
    for ($i = 0; $i -lt $Seconds; $i++) {
        try {
            $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { return }
        } catch { Start-Sleep -Seconds 1 }
    }
    throw "$Name at $Url did not become ready within ${Seconds}s"
}

function Stop-ProcessOnPort {
    param([int]$Port)
    $conn = netstat -ano | Select-String ":$Port\s"
    foreach ($line in $conn) {
        $pid = ($line -split '\s+')[-1]
        if ($pid -match '^\d+$') {
            Write-Warn "Port $Port in use by PID $pid — stopping..."
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
    }
}

# ── Cleanup handler ──
$Script:ChildPids = @()
$CleanupRegistered = $false

function Cleanup-Processes {
    Write-Info "Shutting down ExamOS..."
    foreach ($pid in $Script:ChildPids) {
        if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
    $Script:ChildPids = @()
}
if (-not $CleanupRegistered) {
    Register-EngineEvent -SourceIdentifier ([System.Management.Automation.PsEngineEvent]::Exiting) -Action { Cleanup-Processes } | Out-Null
    $CleanupRegistered = $true
}

# ── Main ──

Write-Info "ExamOS starting..."

# 1. Dependency check
if (-not $SkipDeps) {
    Write-Info "Checking Python dependencies..."
    $deps = @("fastapi", "uvicorn", "httpx", "fsrs")
    foreach ($dep in $deps) {
        $found = python -c "import $dep" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Missing: $dep — installing..."
            pip install $dep -q
        }
    }
    Write-Ok "Python dependencies OK"

    Write-Info "Checking Node dependencies..."
    if (-not (Test-Path "$Root\apps\web\node_modules")) {
        Write-Warn "node_modules missing — running npm install..."
        Push-Location "$Root\apps\web"
        npm install
        Pop-Location
    }
    Write-Ok "Node dependencies OK"

    # 2. Import mock questions (idempotent — skips if already done)
    if (-not (Test-Path "$Root\.system\memory\mock_question_index.json")) {
        Write-Info "Importing mock question bank..."
        $env:PYTHONPATH = "$Root\.system;$Root\apps\api"
        python -c @"
import sys, json
from pathlib import Path
sys.path[0:0] = [r'$Root\.system', r'$Root\apps\api']
from app.mock_ingestion import ingest_all_mock_questions
idx = ingest_all_mock_questions(Path(r'$Root'))
print(f'Mock question bank: {idx["total_questions"]} questions indexed')
"@
        Write-Ok "Mock question bank ready"
    } else {
        Write-Info "Mock question bank already imported (found mock_question_index.json)"
    }
}

# 3. Kill anything on our ports
Stop-ProcessOnPort -Port $ApiPort
Stop-ProcessOnPort -Port $WebPort

# 4. Start API
Write-Info "Starting API on $ApiUrl ..."
$apiProc = Start-Process -FilePath "python" -ArgumentList @(
    "-m", "uvicorn", "main:app",
    "--app-dir", "$Root\apps\api",
    "--host", "0.0.0.0",
    "--port", "$ApiPort"
) -NoNewWindow -PassThru -RedirectStandardOutput "$Root\.system\logs\api.stdout.log" -RedirectStandardError "$Root\.system\logs\api.stderr.log"
$Script:ChildPids += $apiProc.Id
Write-Info "API PID: $($apiProc.Id)"

try {
    Wait-ForUrl -Url "$ApiUrl/api/health" -Name "ExamOS API"
    Write-Ok "API ready → $ApiUrl"

    # 5. Start Web
    $env:NEXT_PUBLIC_API_URL = $ApiUrl
    Write-Info "Starting Web on $WebUrl ..."
    $webProc = Start-Process -FilePath "npx.cmd" -ArgumentList @(
        "next", "dev", "-p", "$WebPort"
    ) -NoNewWindow -PassThru -WorkingDirectory "$Root\apps\web" `
        -RedirectStandardOutput "$Root\.system\logs\web.stdout.log" `
        -RedirectStandardError "$Root\.system\logs\web.stderr.log"
    $Script:ChildPids += $webProc.Id
    Write-Info "Web PID: $($webProc.Id)"

    try {
        Wait-ForUrl -Url "$WebUrl" -Name "ExamOS Web"
        Write-Ok "Web ready → $WebUrl"
        Write-Info ""
        Write-Info "═══════════════════════════════════════════════"
        Write-Info "  ExamOS is running"
        Write-Info "  Web:  $WebUrl"
        Write-Info "  API:  $ApiUrl"
        Write-Info "  Logs: $Root\.system\logs\"
        Write-Info "  Press Ctrl+C to stop all services."
        Write-Info "═══════════════════════════════════════════════"

        if (-not $NoBrowser) { Start-Process $WebUrl }

        # Poll until either process exits
        while ($true) {
            Start-Sleep -Seconds 3
            if ($apiProc.HasExited) { throw "API process exited unexpectedly (code $($apiProc.ExitCode))" }
            if ($webProc.HasExited) { throw "Web process exited unexpectedly (code $($webProc.ExitCode))" }
        }
    } finally {
        if (-not $webProc.HasExited) { $webProc.Kill() }
        $Script:ChildPids = @($apiProc.Id)
    }
} finally {
    if (-not $apiProc.HasExited) { $apiProc.Kill() }
    $Script:ChildPids = @()
}
