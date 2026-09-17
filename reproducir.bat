@echo off
setlocal
cd /d "%~dp0"
if defined M1721_PYTHON (
  "%M1721_PYTHON%" -B src\reproducir.py
) else (
  python -B src\reproducir.py
)
exit /b %errorlevel%
