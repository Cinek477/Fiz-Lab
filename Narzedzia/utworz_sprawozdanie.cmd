@echo off
chcp 65001 >nul
setlocal
if "%~1"=="" (
  echo Przeciagnij zapisany plik XLSX na ten plik CMD.
  echo Instrukcja: Excel/README.md
  pause
  exit /b 2
)
where uv >nul 2>nul
if errorlevel 1 (
  python "%~dp0excel_sprawozdanie.py" "%~f1"
) else (
  uv run "%~dp0excel_sprawozdanie.py" "%~f1"
)
set "FIZLAB_EXIT=%errorlevel%"
echo.
pause
exit /b %FIZLAB_EXIT%
