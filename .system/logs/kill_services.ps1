# Kill services on ports 8000 and 3000
foreach ($port in @(8000, 3000)) {
    netstat -ano | Select-String ":$port\s" | Select-String LISTEN | ForEach-Object {
        $f = ($_ -split '\s+')[-1]
        if ($f -match '^\d+$' -and $f -ne '0') {
            Write-Host "Killing PID $f on port $port"
            Stop-Process -Id $f -Force -ErrorAction SilentlyContinue
        }
    }
}
Write-Host "Done"
