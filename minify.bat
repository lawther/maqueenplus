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
python constant_replacer.py %filename%
python minimal_renamer.py %1-decon.py
pyminify %1-decon-min.py --remove-debug --remove-literal-statements --output .\minified\%filename%
for %%A in (%filename%) do set "orig_filesize=%%~zA"
for %%A in (.\minified\%filename%) do set "minified_filesize=%%~zA"
echo Filesize of %filename% reduced from %orig_filesize% bytes to %minified_filesize% bytes
del %1-decon.py
del %1-decon-min.py
goto :EOF
