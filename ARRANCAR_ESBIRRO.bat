@echo off
title ESBIRRO DEL TERROR - NUCLEO DE MANDO
color 0c

echo ==========================================
echo    ESBIRRO DEL TERROR - NUCLEO DE MANDO
echo ==========================================
echo [!] Iniciando Protocolos del Vacio...
echo [!] Cargando Ojo del Vacio y Servidor de Flask...

:: Abrir la interfaz en el navegador por defecto inmediatamente
start "" "index.html"

:: Ejecutar el servidor (mantiene la ventana abierta para ver logs)
python server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] ERROR: No se pudo iniciar el servidor. 
    echo [!] Asegurate de que Python este en el PATH y Flask instalado.
    pause
)
