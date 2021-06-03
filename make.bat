REM Requires python3.8.bat on the path; this is defined in the top-level project directory
REM conda activate CaseStudy
REM make test
set path=%path%;%CD%
if %1% == test goto test
if %1% == images goto images
goto end

:test
set TOX_OPTIONS=
cmd /c "chdir ch_01&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_02&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_03&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_04&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_05&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_06&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_07&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_08&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_09&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_10&&tox %TOX_OPTIONS%&&tox -e bench&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_11&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_12&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_13&&tox %TOX_OPTIONS%&&tox -e coverage&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
cmd /c "chdir ch_14&&tox %TOX_OPTIONS%&&exit /b %ERRORLEVEL%"
if %ERRORLEVEL% neq 0 goto error
goto end
      
:images
python ch_12\src\images.py
goto end

:error
@echo "Failure"
exit %ERRORLEVEL%

:end
@echo "Done"
