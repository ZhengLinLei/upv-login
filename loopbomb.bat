@echo off

SET COMMAND="python3"

WHERE python3
IF %ERRORLEVEL% NEQ 0 SET COMMAND="python"

for /F "tokens=*" %%A in (users.txt) do %COMMAND% ./bomb.py -u %%A