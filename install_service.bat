@echo off
echo ========================================
echo wxauto API ����װ�ű�
echo ========================================

:: ������ԱȨ��
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ������Ҫ����ԱȨ�����д˽ű�
    echo ���Ҽ�������ļ���ѡ��"�Թ���Ա�������"
    pause
    exit /b 1
)

:: ���ñ���
set SERVICE_NAME=wxautoAPI
set SERVICE_DISPLAY_NAME=wxauto API Service
set SERVICE_DESCRIPTION=΢���Զ���API����
set APP_PATH=%~dp0
set PYTHON_PATH=%APP_PATH%.venv\Scripts\python.exe
set SCRIPT_PATH=%APP_PATH%\run.py

:: ���Python����
if not exist "%PYTHON_PATH%" (
    echo ����δ�ҵ�Python���⻷��
    echo �������� setup.bat ��װ����
    pause
    exit /b 1
)

:: ���������
if not exist "%SCRIPT_PATH%" (
    echo ����δ�ҵ��������ļ�
    pause
    exit /b 1
)

:: ��������ļ�
if not exist "%APP_PATH%config.yaml" (
    echo ���棺δ�ҵ�config.yaml�����ļ�����ʹ��Ĭ������
)

:: ֹͣ��ɾ���Ѵ��ڵķ���
echo ������з���...
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorLevel% equ 0 (
    echo �������з�������ֹͣ...
    net stop "%SERVICE_NAME%" >nul 2>&1
    echo ����ɾ�����з���...
    sc delete "%SERVICE_NAME%" >nul 2>&1
    timeout /t 2 >nul
)

:: ��������
echo ���ڴ���Windows����...
echo ���񽫴�config.yaml��ȡ����...
sc create "%SERVICE_NAME%" binPath= "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" DisplayName= "%SERVICE_DISPLAY_NAME%" start= auto

:: ���÷�������
sc description "%SERVICE_NAME%" "%SERVICE_DESCRIPTION%"

:: ��������
echo ������������...
net start "%SERVICE_NAME%"

:: ������״̬
sc query "%SERVICE_NAME%" | find "RUNNING" >nul
if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo ����װ�ɹ���
    echo ========================================
    echo ��������: %SERVICE_NAME%
    echo ��ʾ����: %SERVICE_DISPLAY_NAME%
    echo �����ļ�: config.yaml
    echo.
    echo ����������
    echo   ��������: net start %SERVICE_NAME%
    echo   ֹͣ����: net stop %SERVICE_NAME%
    echo   ��������: net stop %SERVICE_NAME% && net start %SERVICE_NAME%
    echo   ɾ������: sc delete %SERVICE_NAME%
    echo.
    echo ע�⣺����˿ں�������鿴config.yaml�ļ�
    echo.
) else (
    echo.
    echo ========================================
    echo ����װʧ�ܣ�
    echo ========================================
    echo ���������Ϣ������
    echo.
)

pause 