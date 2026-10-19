@echo off
if "%~1"=="" (
  call "%~dp0..\..\Narzedzia\utworz_sprawozdanie.cmd"
) else (
  call "%~dp0..\..\Narzedzia\utworz_sprawozdanie.cmd" "%~f1"
)
