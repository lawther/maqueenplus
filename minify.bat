@echo off
setlocal

call :minify maqueenplus
call :minify maqueenplusv2
call :minify huskylens
echo Minification complete
goto :EOF

:minify
:: Minify a file and report befoe and after size
set filename=%1.py
python minimal_renamer.py %filename%
pyminify %1-min.py --remove-debug --remove-literal-statements --output .\minified\%filename%
for %%A in (%filename%) do set "orig_filesize=%%~zA"
for %%A in (.\minified\%filename%) do set "minified_filesize=%%~zA"
echo Filesize of %filename% reduced from %orig_filesize% bytes to %minified_filesize% bytes
del %1-min.py
goto :EOF
