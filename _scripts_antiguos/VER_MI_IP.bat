@echo off
echo.
echo ========================================
echo  Informacion de Red - Sistema DHL
echo ========================================
echo.

echo Tu direccion IP para acceso desde otras PCs:
echo.
ipconfig | findstr /i "IPv4"

echo.
echo ========================================
echo Instrucciones para otras PCs:
echo ========================================
echo.
echo 1. Copia la IP que aparece arriba
echo 2. Desde otra PC, abre el navegador
echo 3. Escribe: http://TU-IP:5000
echo.
echo Ejemplo: http://192.168.1.100:5000
echo.
echo ========================================
echo.
echo Estado del puerto 5000:
netstat -an | findstr :5000

echo.
echo ========================================
echo.
pause
