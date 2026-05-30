# Start ExamOS API and Web with one command.
param(
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$ApiUrl = "http://127.0.0.1:$ApiPort"
$WebUrl = "http://127.0.0.1:$WebPort"

function Wait-ForUrl {
    param(
        [string]$Url,
        [string]$Name,
        [int]$Seconds = 60
    )

    for ($i = 0; $i -lt $Seconds; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                return
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }

    throw "$Name did not become ready at $Url"
}

Write-Host "Starting ExamOS..." -ForegroundColor Cyan

$apiJob = Start-Job -Name "ExamOS API" -ArgumentList $Root, $ApiPort -ScriptBlock {
    param($Root, $ApiPort)
    Set-Location $Root
    .\start-api.ps1 -Port $ApiPort
}

try {
    Wait-ForUrl -Url "$ApiUrl/api/health" -Name "ExamOS API"
    Write-Host "API ready: $ApiUrl" -ForegroundColor Green

    $webJob = Start-Job -Name "ExamOS Web" -ArgumentList $Root, $WebPort, $ApiUrl -ScriptBlock {
        param($Root, $WebPort, $ApiUrl)
        Set-Location $Root
        $env:NEXT_PUBLIC_API_URL = $ApiUrl
        .\start-web.ps1 -Port $WebPort
    }

    try {
        Wait-ForUrl -Url "$WebUrl/today" -Name "ExamOS Web"
        Write-Host "Web ready: $WebUrl" -ForegroundColor Green
        Write-Host ""
        Write-Host "Open ExamOS: $WebUrl" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C in this window to stop API + Web." -ForegroundColor DarkGray

        if (-not $NoBrowser) {
            Start-Process $WebUrl
        }

        while ($true) {
            Start-Sleep -Seconds 2

            foreach ($job in @($apiJob, $webJob)) {
                if ($job.State -in @("Failed", "Stopped", "Completed")) {
                    Receive-Job $job -Keep
                    throw "$($job.Name) stopped unexpectedly."
                }
            }
        }
    } finally {
        if ($webJob) {
            Stop-Job $webJob -ErrorAction SilentlyContinue
            Remove-Job $webJob -Force -ErrorAction SilentlyContinue
        }
    }
} finally {
    if ($apiJob) {
        Stop-Job $apiJob -ErrorAction SilentlyContinue
        Remove-Job $apiJob -Force -ErrorAction SilentlyContinue
    }
}
