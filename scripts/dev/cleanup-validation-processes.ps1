param(
  [string[]]$Ports = @("8000", "3010"),
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Get-PortOwners {
  param([int[]]$PortList)
  $connections = @()
  foreach ($port in $PortList) {
    $connections += @(Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue)
  }
  $connections |
    Where-Object { $_.State -eq "Listen" -and $_.OwningProcess -gt 0 } |
    Select-Object LocalPort, State, OwningProcess -Unique
}

$normalizedPorts = @(
  foreach ($item in $Ports) {
    foreach ($part in ($item -split ",")) {
      $text = $part.Trim()
      if ($text) { [int]$text }
    }
  }
) | Select-Object -Unique

$owners = @(Get-PortOwners -PortList $normalizedPorts)
if ($owners.Count -eq 0) {
  Write-Output "No listening validation processes found for ports: $($normalizedPorts -join ', ')"
} else {
  foreach ($owner in $owners) {
    $process = Get-Process -Id $owner.OwningProcess -ErrorAction SilentlyContinue
    $name = if ($process) { $process.ProcessName } else { "unknown" }
    if ($DryRun) {
      Write-Output "Would stop PID $($owner.OwningProcess) ($name) on port $($owner.LocalPort)"
      continue
    }
    Stop-Process -Id $owner.OwningProcess -Force -ErrorAction SilentlyContinue
    Write-Output "Stopped PID $($owner.OwningProcess) ($name) on port $($owner.LocalPort)"
  }
}

Start-Sleep -Milliseconds 500
$remaining = @(Get-PortOwners -PortList $normalizedPorts)
if ($remaining.Count -eq 0) {
  Write-Output "Ports released: $($normalizedPorts -join ', ')"
} else {
  Write-Output "Lingering listeners:"
  $remaining | ForEach-Object {
    Write-Output "port=$($_.LocalPort) pid=$($_.OwningProcess) state=$($_.State)"
  }
}
