@echo off
chcp 936 >nul
echo ========================================
echo wxauto API ����ж�ؽű�
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

:: �������Ƿ����
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorLevel% neq 0 (
    echo ���� %SERVICE_NAME% �����ڣ�����ж��
    pause
    exit /b 0
)

:: ֹͣ����
echo ����ֹͣ����...
net stop "%SERVICE_NAME%" >nul 2>&1

:: ɾ������
echo ����ɾ������...
sc delete "%SERVICE_NAME%"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo ����ж�سɹ���
    echo ========================================
    echo ���� %SERVICE_NAME% �ѱ���ȫ�Ƴ�
    echo.
) else (
    echo.
    echo ========================================
    echo ����ж��ʧ�ܣ�
    echo ========================================
    echo ���������Ϣ������
    echo.
)

pause 