@echo off
setlocal

rem Ensure UTF-8 code page is active
for /f "tokens=2 delims=:." %%a in ("%SystemRoot%\System32\chcp.com") do (
    set "_OLD_CODEPAGE=%%a"
)
if defined _OLD_CODEPAGE (
    chcp 65001 > nul
)

rem Dynamically get the directory this script is in and set it as VIRTUAL_ENV
set "SCRIPT_DIR=%~dp0"
set "VIRTUAL_ENV=%SCRIPT_DIR%.."

rem Save and update PROMPT
if not defined PROMPT set "PROMPT=$P$G"
if defined _OLD_VIRTUAL_PROMPT set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
set "PROMPT=(venv) %PROMPT%"

rem Save and unset PYTHONHOME
if defined PYTHONHOME set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
set "PYTHONHOME="

rem Save and update PATH
if defined _OLD_VIRTUAL_PATH set "PATH=%_OLD_VIRTUAL_PATH%"
if not defined _OLD_VIRTUAL_PATH set "_OLD_VIRTUAL_PATH=%PATH%"
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set "VIRTUAL_ENV_PROMPT=(venv)"

:END
rem Restore original code page
if defined _OLD_CODEPAGE (
    chcp %_OLD_CODEPAGE% > nul
    set "_OLD_CODEPAGE="
)
endlocal & (
    set "VIRTUAL_ENV=%VIRTUAL_ENV%"
    set "PATH=%PATH%"
    set "PROMPT=%PROMPT%"
    set "PYTHONHOME=%PYTHONHOME%"
    set "VIRTUAL_ENV_PROMPT=%VIRTUAL_ENV_PROMPT%"
    set "_OLD_VIRTUAL_PROMPT=%_OLD_VIRTUAL_PROMPT%"
    set "_OLD_VIRTUAL_PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%"
    set "_OLD_VIRTUAL_PATH=%_OLD_VIRTUAL_PATH%"
)
