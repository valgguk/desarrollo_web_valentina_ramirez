# Script para iniciar Flask y Spring Boot en ventanas separadas

Write-Host "🚀 Iniciando aplicaciones..." -ForegroundColor Green

# 1. Flask en nueva ventana
Write-Host "📦 Iniciando Flask (puerto 5000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\.venv\Scripts\Activate.ps1; python run.py }"

# 2. Esperar 3 segundos
Start-Sleep -Seconds 3

# 3. Spring Boot en nueva ventana
Write-Host "☕ Iniciando Spring Boot (puerto 8080)..." -ForegroundColor Yellow
Set-Location "adopcion-mascotas"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "mvn spring-boot:run"
Set-Location ..

Write-Host "`n✅ Aplicaciones iniciadas en ventanas separadas:" -ForegroundColor Green
Write-Host "   🐍 Flask:       http://localhost:5000/" -ForegroundColor Cyan
Write-Host "   ☕ Spring Boot: http://localhost:8080/evaluacion" -ForegroundColor Yellow
Write-Host "`n⚠️  Cierra las ventanas de PowerShell para detener las aplicaciones" -ForegroundColor Red
