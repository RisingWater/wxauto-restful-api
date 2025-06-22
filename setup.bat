@echo off
chcp 65001 >nul
echo ========================================
echo wxauto API �������ýű�
echo ========================================

:: ���Python�汾
echo ���Python����...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ����δ�ҵ�Python�����Ȱ�װPython 3.11+
    echo ���ص�ַ��https://www.python.org/downloads/
    pause
    exit /b 1
)

:: ���uv�Ƿ�װ
echo ���uv��������...
uv --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ���ڰ�װuv��������...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if %errorLevel% neq 0 (
        echo ����uv��װʧ�ܣ����ֶ���װ
        echo ��װ���pip install uv
        pause
        exit /b 1
    )
)

:: �������⻷������װ����
echo ���ڴ������⻷������װ����...
uv sync

if %errorLevel% neq 0 (
    echo ����������װʧ��
    pause
    exit /b 1
)

:: ������Ҫ��Ŀ¼
echo ������Ҫ��Ŀ¼...
if not exist "data" mkdir data
if not exist "uploads" mkdir uploads
if not exist "wxauto_logs" mkdir wxauto_logs

:: ��������ļ�
if not exist "config.yaml" (
    echo ���棺δ�ҵ�config.yaml�����ļ�
    echo ��ʹ��Ĭ������
)

:: �������⻷��������
echo ���Ի���...
call .venv\Scripts\activate.bat
python -c "import fastapi, wxautox; print('�������Գɹ���')"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo ����������ɣ�
    echo ========================================
    echo ���ڿ��������������
    echo   ��������: run.bat
    echo   ��װΪWindows����: install_service.bat (��Ҫ����ԱȨ��)
    echo.
) else (
    echo.
    echo ========================================
    echo ��������ʧ�ܣ�
    echo ========================================
    echo ���������Ϣ������
    echo.
)

pause 