@echo off
cd /d "%~dp0"
echo ============================================
echo   Art Exhibition - Client and Admin Alag
echo ============================================
echo   Client:  http://127.0.0.1:8001/
echo   Admin:   http://127.0.0.1:8001/admin-panel/
echo ============================================
start http://127.0.0.1:8001
python manage.py runserver 8001
pause
