@echo off
echo ========================================
echo wxauto API ���ò��Խű�
echo ========================================

:: ������⻷��
if not exist ".venv\Scripts\python.exe" (
    echo ����δ�ҵ����⻷��
    echo �������� setup.bat ��װ����
    pause
    exit /b 1
)

:: �������⻷�����������ò���
echo ���ڲ�������ϵͳ...
call .venv\Scripts\activate.bat
python test_config.py

if %errorLevel% equ 0 (
    echo.
    echo ���ò���ͨ����
) else (
    echo.
    echo ���ò���ʧ�ܣ����������Ϣ
)

pause 