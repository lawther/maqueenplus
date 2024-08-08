@echo off
setlocal

call :minify maqueenplus.py
call :minify maqueenplus_v2.py
call :minify huskylens.py
echo Minification complete
goto :EOF

:minify
:: Minify a file and report befoe and after size
pyminify %1 --remove-debug --remove-literal-statements --output .\minified\%1
for %%A in (%1) do set "orig_filesize=%%~zA"
for %%A in (.\minified\%1) do set "minified_filesize=%%~zA"
echo Filesize of %1 reduced from %orig_filesize% bytes to %minified_filesize% bytes
goto :EOF
