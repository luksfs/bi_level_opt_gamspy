REM python direct_4D_DSDA.py
REM if %errorlevel% neq 0 exit /b %errorlevel%
REM python direct_5D_DSDA.py
REM if %errorlevel% neq 0 exit /b %errorlevel%
python direct_7D_DSDA.py
if %errorlevel% neq 0 exit /b %errorlevel%
python direct_6D_DSDA.py