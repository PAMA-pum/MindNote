@echo off
rem Start the Flask app in this repository via the Python launcher or python
pushd %~dp0
if exist "%SystemRoot%\py.exe" (
  "%SystemRoot%\py.exe" -3 app.py
) else (
  python app.py
)
pause