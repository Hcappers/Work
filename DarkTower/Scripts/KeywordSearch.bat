:: Description: Searches for files containing a keyword or multiple keywords from a file in a directory and its subdirectories.
:: Usage: KeywordSearch.bat [directory] or KeywordSearch.bat
:: Written by Alex Cappers on 2024-12-24.

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
    pause
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

:: Prompt the user for a single keyword or file
PowerShell -Command "Write-Host '[NOTE] Would you like to search for a single keyword or use a file of keywords? Enter 1 for single keyword or 2 for file:' -ForegroundColor Yellow"
set /p SearchOption=

:: Process the user's choice. Not sure why this way worked and doing if/else if didn't.
goto case_%SearchOption%

:case_1
:: Single keyword search
PowerShell -Command "Write-Host '[NOTE] Please enter the keyword to search for:' -ForegroundColor Yellow"
set /p SearchKeyword=
PowerShell -Command "Write-Host '[ACTION] Searching for keyword: ''%SearchKeyword%''...' -ForegroundColor Cyan"

:: Run PowerShell command for the single keyword
    PowerShell -Command "$normalizedKeyword = ('%SearchKeyword%' -replace '[-\s]', ''); $matches = Get-ChildItem -Path '%SearchDir%' -Recurse | Where-Object { ($_.FullName -replace '[-\s]', '') -match $normalizedKeyword }; Write-Host '[FOUND] Total matches for keyword ''%SearchKeyword%'': ' $matches.Count -ForegroundColor White; $matches.FullName | Out-File -Append -FilePath '%ResultFile%' -Encoding ASCII"
goto end

:case_2
:: File of keywords search
PowerShell -Command "Write-Host '[NOTE] Please enter the directory containing the file of keywords:' -ForegroundColor Yellow"
set /p KeywordDir=

:: Verify the directory exists
if not exist "%KeywordDir%" (
    PowerShell -Command "Write-Host '[ERROR] The specified directory does not exist: %KeywordDir%' -ForegroundColor Red"
    pause
    exit /b 1
)

:: Prompt for the file name
PowerShell -Command "Write-Host '[NOTE] Please enter the file name in ''%KeywordDir%'' (including extension):' -ForegroundColor Yellow"
set /p KeywordFileName=

:: Combine directory and file name
set KeywordFile=%KeywordDir%\%KeywordFileName%

:: Verify the keyword file exists
if not exist "%KeywordFile%" (
    PowerShell -Command "Write-Host '[ERROR] The specified keyword file does not exist: %KeywordFile%' -ForegroundColor Red"
    pause
    exit /b 1
)

PowerShell -Command "Write-Host '[DEBUG] Reading keywords from file: ''%KeywordFile%''.' -ForegroundColor Yellow"

:: Process keywords from file
for /f "usebackq delims=" %%K in ("%KeywordFile%") do (
    :: Show current keyword being searched
    PowerShell -Command "Write-Host '[ACTION] Searching for keyword: ''%%K''...' -ForegroundColor Cyan"

    :: Search for the keyword in the directory and its subdirectories, output the total matches found and save to the result file.
    PowerShell -Command "$normalizedKeyword = ('%%K' -replace '[-\s]', ''); $matches = Get-ChildItem -Path '%SearchDir%' -Recurse | Where-Object { ($_.FullName -replace '[-\s]', '') -match $normalizedKeyword }; Write-Host '[FOUND] Total matches for keyword ''%%K'': ' $matches.Count -ForegroundColor White; $matches.FullName | Out-File -Append -FilePath '%ResultFile%' -Encoding ASCII"
)
goto end

:default
PowerShell -Command "Write-Host '[ERROR] Invalid option. Please enter 1 for single keyword or 2 for file.' -ForegroundColor Red"
pause
goto end

:end
:: Completion message
PowerShell -Command "Write-Host '[OK] Search completed. Results saved in ''%ResultFile%''.' -ForegroundColor Green"
pause
exit /b