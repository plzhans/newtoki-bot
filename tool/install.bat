@ECHO OFF

ECHO.
ECHO ===============================
ECHO = Start install
ECHO ===============================

SET CHROME_DRIVER_VERSION=%CHROME_DRIVER_VERSION%
IF "%CHROME_DRIVER_VERSION%" == "" (
    SET CHROME_DRIVER_VERSION=98.0.4758.48
)

SET CHROME_DRIVER_BASE_URL=https://chromedriver.storage.googleapis.com/%CHROME_DRIVER_VERSION%

ECHO.
ECHO chrome driver downloading... chromedriver_win32.zip
ECHO ______________________________
ECHO.
curl --create-dirs %CHROME_DRIVER_BASE_URL%/chromedriver_win32.zip -o .\temp\chromedriver_win32.zip
ECHO.