# PowerShell script - Activate virtual environment and set PYTHONPATH
Write-Host "Activating virtual environment..." -ForegroundColor Green
. .\.venv\Scripts\activate.ps1
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host "Current virtual environment: $env:VIRTUAL_ENV_PROMPT" -ForegroundColor Yellow

# Set PYTHONPATH
$env:PYTHONPATH = "D:\code\ollama-search-agent"
Write-Host "PYTHONPATH set to: $env:PYTHONPATH" -ForegroundColor Cyan
