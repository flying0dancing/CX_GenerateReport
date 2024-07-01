@echo off
set _WorkSpace=%~dp0
echo %_WorkSpace%reporter_template.exe reporter_template.json YYT1818_SingleRun
%_WorkSpace%reporter_template.exe reporter_template.json YYT1818_SingleRun
@echo on
pause ...