@echo off
setlocal enabledelayedexpansion

REM This script updates the .env file FOR WINDOWS with the IP address obtained from the hostname -I command.
REM It ensures that the ALLOWED_HOSTS value contains the static IP addresses 127.0.0.1 and 0.0.0.0, 
REM as well as the IP address returned by the command.
REM If the .env file does not exist, it copies from .env.sample.

REM The purpose of this procedure is to ensure that by starting the application in the terminal 
REM (e.g. linux sever VM) you will be able to run it on a browser on a device located in a given network
REM (browser on a phone)

REM Initialize IP_ADDRESSES variable
set IP_ADDRESSES=

REM Get all IP addresses using the ipconfig command and find the IPv4 address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set IP_ADDRESSES=!IP_ADDRESSES!%%a
)

REM Construct the value for ALLOWED_HOSTS
set ALLOWED_HOSTS_VALUE=ALLOWED_HOSTS=app 127.0.0.1 0.0.0.0!IP_ADDRESSES!

REM Path to the .env file in the parent directory
set ENV_PATH=.\.env
set ENV_SAMPLE_PATH=.\.env.sample

REM Check if the .env file exists
if not exist %ENV_PATH% (
    REM If it doesn't exist, copy .env.sample to .env in the parent directory
    copy %ENV_SAMPLE_PATH% %ENV_PATH%
)

REM Check if ALLOWED_HOSTS exists in the .env file
findstr /m "ALLOWED_HOSTS" %ENV_PATH%
if %errorlevel%==0 (
    REM If it exists, update the value
    powershell -Command "(Get-Content %ENV_PATH%) -replace 'ALLOWED_HOSTS=.*', '%ALLOWED_HOSTS_VALUE%' | Set-Content %ENV_PATH%"
)