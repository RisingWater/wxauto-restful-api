@echo off
echo ========================================
echo wxauto API ���ü��ű�
echo ========================================

:: ������⻷��
if not exist ".venv\Scripts\python.exe" (
    echo ����δ�ҵ����⻷��
    echo �������� setup.bat ��װ����
    pause
    exit /b 1
)

:: �������⻷�����������ü��
echo ���ڼ������...
call .venv\Scripts\activate.bat
python check_config.py

pause 