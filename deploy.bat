@echo off
chcp 936 >nul
echo ========================================
echo wxauto API һ������ű�
echo ========================================

:: ������ԱȨ��
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ������Ҫ����ԱȨ�����д˽ű�
    echo ���Ҽ�������ļ���ѡ��"�Թ���Ա�������"
    pause
    exit /b 1
)

echo ����1: ��������...
call setup.bat
if %errorLevel% neq 0 (
    echo ��������ʧ�ܣ�������ֹ
    pause
    exit /b 1
)

echo.
echo ����2: ��װWindows����...
call install_service.bat
if %errorLevel% neq 0 (
    echo ����װʧ�ܣ�������ֹ
    pause
    exit /b 1
)

echo.
echo ========================================
echo һ��������ɣ�
echo ========================================
echo.
echo ������Ϣ��
echo   - ��������: wxautoAPI
echo   - �����ļ�: config.yaml
echo   - ״̬: �Զ�����
echo.
echo �������
echo   - ��������: net start wxautoAPI
echo   - ֹͣ����: net stop wxautoAPI
echo   - ��������: net stop wxautoAPI && net start wxautoAPI
echo   - ж�ط���: uninstall_service.bat
echo.
echo ����˵����
echo   - �������˿ں�������༭ config.yaml �ļ�
echo   - �޸����ú���Ҫ��������
echo.
echo ������ϵͳ����ʱ�Զ�����
echo �����޸����ã���༭ config.yaml �ļ�
echo.

pause 