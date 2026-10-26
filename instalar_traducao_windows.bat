@echo off
setlocal
chcp 65001 >nul
title Instalador Traducao PT-BR - Dragon's Crown Pro
echo =====================================================================
echo       TRADUCAO PORTUGUES BRASILEIRO (PT-BR) - DRAGON'S CROWN PRO
echo                     (Dragon's Crown Pro - Recomp PC)
echo =====================================================================
echo.

rem Python 3: o launcher "py" primeiro; "python" so se for um Python de verdade (nao o atalho da Microsoft Store).
set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERRO] Python 3 nao encontrado.
    echo Instale em https://www.python.org/downloads/ marcando "Add python.exe to PATH" e rode de novo.
    echo.
    pause
    exit /b 1
)

rem Caminho opcional: a pasta do jogo ou o DRACRO_US.CPK, arrastado sobre este .bat. Sem ele, o patcher procura sozinho
rem e, se nao achar, pergunta.
set "TARGET=%~1"

%PY% "%~dp0ferramentas\patcher.py" apply "%TARGET%" "%~dp0arquivos_traducao"
set "RESULT=%errorlevel%"

echo.
if "%RESULT%"=="0" (
    echo [SUCESSO] Traducao PT-BR instalada! No launcher, mantenha o idioma em English.
    echo Para remover, use desinstalar_traducao_windows.bat.
) else (
    echo [ERRO] Nada foi alterado ou a operacao nao terminou. Veja a mensagem acima.
)
echo.
pause
exit /b %RESULT%
