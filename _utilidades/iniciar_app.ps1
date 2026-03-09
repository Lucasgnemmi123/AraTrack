# Script PowerShell para iniciar la aplicación con output capturado
$ErrorActionPreference = "Continue"
$scriptPath = $PSScriptRoot
Set-Location $scriptPath

Write-Host "="*60
Write-Host "Iniciando Sistema de Viajes DHL"
Write-Host "="*60
Write-Host ""

# Activar entorno
& "$scriptPath\.venv\Scripts\Activate.ps1"

# Establecer variables de entorno
$env:ARATRACK_ENV = "production"

Write-Host "Ejecutando app_web.py..."
Write-Host "Output se guardará en: app_output.log"
Write-Host ""

# Ejecutar Python y capturar output
$process = Start-Process -FilePath "$scriptPath\.venv\Scripts\python.exe" `
                          -ArgumentList "$scriptPath\app_web.py" `
                          -WorkingDirectory $scriptPath `
                          -RedirectStandardOutput "$scriptPath\app_output.log" `
                          -RedirectStandardError "$scriptPath\app_errors.log" `
                          -NoNewWindow `
                          -PassThru

Write-Host "Proceso iniciado con PID: $($process.Id)"
Write-Host ""
Write-Host "Esperando 3 segundos para verificar inicio..."
Start-Sleep -Seconds 3

if (!$process.HasExited) {
    Write-Host "✓ Aplicación corriendo"
    Write-Host ""
    Write-Host "Para ver el output:"
    Write-Host "  type app_output.log"
    Write-Host ""
    Write-Host "Para ver errores:"
    Write-Host "  type app_errors.log"
    Write-Host ""
    Write-Host "Para detener el servidor:"
    Write-Host "  Stop-Process -Id $($process.Id)"
} else {
    Write-Host "✗ La aplicación se detuvo"
    Write-Host ""
    Write-Host "Errores:"
    Get-Content "$scriptPath\app_errors.log"
}
