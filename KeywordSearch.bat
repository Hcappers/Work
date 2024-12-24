:: Description: Searches for files containing a keyword in a directory and its subdirectories.
:: Usage: KeywordSearch.bat [directory] or KeywordSearch.bat
:: Written by Alex Cappers (https://github.com/HCappers/Work) on 2024-12-24

@echo off
setlocal enabledelayedexpansion

:: Prompt for directory if not provided as an argument
if "%~1"=="" (
    PowerShell -Command "Write-Host '[NOTE] Please enter the directory to search:' -ForegroundColor Yellow"
    set /p SearchDir=
) else (
    set SearchDir=%~1
)

:: Verify the directory exists
if not exist "%SearchDir%" (
    PowerShell -Command "Write-Host '[ERROR] The specified directory does not exist: %SearchDir%' -ForegroundColor Red"
    exit /b 1
)

:: Prompt for result file name
PowerShell -Command "Write-Host '[NOTE] Please enter the name for the result file (without extension):' -ForegroundColor Yellow"
set /p ResultFile=
set "ResultFile=%ResultFile: =_%"
set ResultFile=%ResultFile%.txt
PowerShell -Command "Write-Host '[NOTE] File name spaces replaced with underscores: ''%ResultFile%''.' -ForegroundColor Yellow"

:: Create the result file
echo. > %ResultFile%
PowerShell -Command "Write-Host '[OK] Result file ''%ResultFile%'' created successfully.' -ForegroundColor Green"

:: Prompt for keyword
PowerShell -Command "Write-Host '[NOTE] Please enter the keyword to search for:' -ForegroundColor Yellow"
set /p SearchKeyword=

:: Debug: Show search info
PowerShell -Command "Write-Host '[DEBUG] Searching in: ''%SearchDir%'' for keyword: ''%SearchKeyword%''.' -ForegroundColor Yellow"

:: Run the search with flexible matching for spaces and hyphens, outputting correctly to the file
PowerShell -Command "$normalizedKeyword = ('%SearchKeyword%' -replace '[-\s]', ''); Get-ChildItem -Path '%SearchDir%' -Recurse -File | Where-Object { ($_.Name -replace '[-\s]', '') -match $normalizedKeyword } | ForEach-Object { Write-Host 'Found: ' $_.FullName -ForegroundColor Cyan; $_.FullName } | Out-File -FilePath '%ResultFile%' -Encoding ASCII"

:: Completion message
PowerShell -Command "Write-Host '[OK] Search completed. Results saved in ''%ResultFile%''.' -ForegroundColor Green"
exit /b 0
