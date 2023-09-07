@echo off
REM This script updates the .env file FOR WINDOWS with the IP address obtained from the hostname -I command.
REM It ensures that the ALLOWED_HOSTS value contains the static IP addresses 127.0.0.1 and 0.0.0.0, 
REM as well as the IP address returned by the command.
REM If the .env file does not exist, it copies from .env.sample.

REM The purpose of this procedure is to ensure that by starting the application in the terminal 
REM (e.g. linux sever VM) you will be able to run it on a browser on a device located in a given network
REM (browser on a phone)

REM Get the IP address using the ipconfig command and find the IPv4 address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4 Address"') do set IP_ADDRESSES=%%a

REM Construct the value for ALLOWED_HOSTS
set ALLOWED_HOSTS_VALUE=ALLOWED_HOSTS=127.0.0.1 0.0.0.0%IP_ADDRESSES%

REM Check if the .env file exists
if not exist .env (
    REM If it doesn't exist, copy .env.sample to .env
    copy .env.sample .env
)

REM Check if ALLOWED_HOSTS exists in the .env file
findstr /m "ALLOWED_HOSTS" .env
if %errorlevel%==0 (
    REM If it exists, update the value
    powershell -Command "(Get-Content .env) -replace 'ALLOWED_HOSTS=.*', '%ALLOWED_HOSTS_VALUE%' | Set-Content .env"
) else (
    REM If it doesn't exist, add to the .env file
    echo %ALLOWED_HOSTS_VALUE% >> .env
)


