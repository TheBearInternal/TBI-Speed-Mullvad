@echo off
title TBI Speed for Mullvad
python "%~dp0tbi_speed.py" %*
if errorlevel 1 pause
