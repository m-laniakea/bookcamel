@ECHO OFF
PUSHD %~dp0

:start

:: Get the preferred method of startup from the user
CLS
ECHO.
ECHO Select a startup option:
ECHO.
ECHO (r) Run server
ECHO (t) Start tests
ECHO (p) Go to the NV prompt
SET /p choice= 

CLS
ECHO Preparing Python prerequisites...

:: Show Windows and Python where to find our Python executables
SET PATH=%PATH%;%SYSTEMDRIVE%\Python27;%SYSTEMDRIVE%\Python27\Lib;%SYSTEMDRIVE%\Python27\DLLs;%SYSTEMDRIVE%\Python27\Scripts
SET PYTHONPATH=%SYSTEMDRIVE%\Python27;%SYSTEMDRIVE%\Python27\Lib;%SYSTEMDRIVE%\Python27\DLLs;%SYSTEMDRIVE%\Python27\Scripts
SET PYTHONHOME=%SYSTEMDRIVE%\Python27

:: Check for prerequisite components
where /q python
IF ERRORLEVEL 1 (
    ECHO WARNING: Python could not be found. Make sure Python 2.7 is installed in %SYSTEMDRIVE%\Python27\ and that you have sufficient privileges.
	PAUSE
	GOTO end
)
where /q pip
IF ERRORLEVEL 1 (
    ECHO WARNING: Python PIP could not be found. Make sure Python 2.7 is installed in %SYSTEMDRIVE%\Python27\ and that you have sufficient privileges.
	PAUSE
	GOTO end
)

:: Installs Python virtual environment, creates and activates one for v2.7
pip install virtualenv
virtualenv-2.7 nv
call nv\Scripts\activate.bat

:: Install prerequisites (in the virtual environment)
pip install -r reqs.txt

:: Decide what to do based on user input above
IF %CHOICE%==r GOTO runserver
IF %CHOICE%==t GOTO testing
IF %CHOICE%==p GOTO prompt
ELSE GOTO badchoice
GOTO end

:runserver
ECHO.
ECHO Starting BookCamel webserver...
ECHO.
SET RUN_MODE=default
python cmd.py runserver
PAUSE
GOTO end

:testing
CLS
ECHO.
ECHO Starting BookCamel testing harness...
ECHO.
SET RUN_MODE=test
python cmd.py test
SET /p this_pauses=Press return to test again (Ctrl+C exits)
GOTO testing

:prompt
CLS
ECHO.
ECHO Starting NV prompt...
ECHO.
cmd /k
GOTO end

:badchoice
ECHO No startup option found for %CHOICE%

:end
deactivate
POPD
