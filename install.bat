@echo off
chcp 65001 >nul
setlocal
rem FragClean installer: copies the plugin source into ZStartup\ZPlugs64.
rem Then in ZBrush: ZScript > Load (Ctrl+Shift+L) > ZStartup\ZPlugs64\FragClean.txt once.
rem Usage: install.bat                                  (asks for language, default folders)
rem        install.bat zh|en "X:\path\ZBrush 2025" 2025 (language, custom folder, version)

set "HERE=%~dp0"
rem temp folder for the OBJ round trip (ZScript cannot create folders)
if not exist "C:\Users\Public\Documents\ZBFragClean" mkdir "C:\Users\Public\Documents\ZBFragClean"

set "LANG=%~1"
if "%LANG%"=="" (
  echo 请选择插件语言 / Choose the plugin language:
  echo   1 = 中文 ^(Z插件 -^> 碎面清理^)
  echo   2 = English ^(ZPlugin -^> FragClean^)
  choice /c 12 /n /m "1 / 2 : "
  if errorlevel 2 (set "LANG=en") else (set "LANG=zh")
)
if /i not "%LANG%"=="zh" if /i not "%LANG%"=="en" (
  echo Unknown language "%LANG%". Use zh or en.
  goto done
)

if not "%~2"=="" (
  call :inst "%~2" "%~3"
  goto done
)

set "FOUND=0"
call :inst "D:\media work\Zbrush2025.0.1" 2025
call :inst "D:\media work\ZBrush 2022.0.5" 2022
call :inst "C:\Program Files\Maxon ZBrush 2025" 2025
call :inst "C:\Program Files\Maxon ZBrush 2024" 2025
call :inst "C:\Program Files\Maxon ZBrush 2023" 2025
call :inst "C:\Program Files\Pixologic\ZBrush 2022" 2022

:ask
if not "%FOUND%"=="0" goto done
echo.
echo 没在常见位置找到 ZBrush。请把 ZBrush 的安装文件夹（里面有 ZBrush.exe 的那个）拖进这个窗口，然后按回车：
echo ZBrush was not found in the usual places. Drag your ZBrush folder ^(the one with ZBrush.exe^) into this window and press Enter:
set "DIR="
set /p "DIR=> "
if not defined DIR goto done
set "DIR=%DIR:"=%"
set "VER=2025"
if not "%DIR:2022=%"=="%DIR%" set "VER=2022"
if not exist "%DIR%\ZStartup\ZPlugs64" (
  echo [!] 这个文件夹里没有 ZStartup\ZPlugs64，请重新拖一次。 / No ZStartup\ZPlugs64 in that folder, try again.
  goto ask
)
call :inst "%DIR%" %VER%
goto done

:inst
if not exist "%~1\ZStartup\ZPlugs64" goto :eof
set "VER=%~2"
if "%VER%"=="" set "VER=2025"
copy /Y "%HERE%build\%LANG%\%VER%\FragClean.txt" "%~1\ZStartup\ZPlugs64\FragClean.txt" >nul
if errorlevel 1 (
  echo [!] 复制失败，请右键 install.bat 选「以管理员身份运行」。 / Copy failed, run install.bat as administrator.
  goto :eof
)
if exist "%~1\ZStartup\ZPlugs64\FragClean.zsc" del /F /Q "%~1\ZStartup\ZPlugs64\FragClean.zsc"
set /a FOUND+=1
echo [OK] %~1  (ZBrush %VER%, %LANG%)
goto :eof

:done
echo.
echo 完成。打开 ZBrush，按 Ctrl+Shift+L 加载 ZStartup\ZPlugs64\FragClean.txt 一次。
echo Done. In ZBrush press Ctrl+Shift+L and load ZStartup\ZPlugs64\FragClean.txt once.
pause
