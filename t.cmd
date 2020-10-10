@echo off &setlocal
set "flag="
(for /f "tokens=1*delims=:" %%a in ('netsh wlan show profiles') do (
    if "%%a"=="User profiles" set flag=true
    if defined flag if "%%~b" neq "" (
        for /f "tokens=*" %%c in ("%%~b") do echo(%%c
    )
))>out.txt
type out.txt