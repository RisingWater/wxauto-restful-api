@echo off

:: ������⻷��
if not exist ".venv\Scripts\python.exe" (
    echo    �X�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�[
    echo    �U                        ������Ϣ                               �U
    echo    �^�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�a
    echo.
    echo    ����δ�ҵ����⻷��
    echo    �������� setup.bat ��װ����
    echo.
    pause
    exit /b 1
)

:: ��������ļ�
if not exist "config.yaml" (
    echo    �X�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�[
    echo    �U                        ������Ϣ                               �U
    echo    �^�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�a
    echo.
    echo    ���棺δ�ҵ�config.yaml�����ļ�����ʹ��Ĭ������
    echo.
)

:: �������⻷������������
echo    �X�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�[
echo    �U                        ������Ϣ                               �U
echo    �^�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�a
echo.
echo    ������������...
echo    ����config.yaml��ȡ����������...
echo.
call .venv\Scripts\activate.bat
echo.
echo    �X�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�[
echo    �U                    wxauto API ���������ű�                    �U
echo    �U                                                              �U
echo    �U   �����[    �����[�����[  �����[ �����������[ �����[   �����[�����������������[ �������������[       �U
echo    �U   �����U    �����U�^�����[�����X�a�����X�T�T�����[�����U   �����U�^�T�T�����X�T�T�a�����X�T�T�T�����[      �U
echo    �U   �����U ���[ �����U �^�������X�a ���������������U�����U   �����U   �����U   �����U   �����U      �U
echo    �U   �����U�������[�����U �����X�����[ �����X�T�T�����U�����U   �����U   �����U   �����U   �����U      �U
echo    �U   �^�������X�������X�a�����X�a �����[�����U  �����U�^�������������X�a   �����U   �^�������������X�a      �U
echo    �U    �^�T�T�a�^�T�T�a �^�T�a  �^�T�a�^�T�a  �^�T�a �^�T�T�T�T�T�a    �^�T�a    �^�T�T�T�T�T�a       �U
echo    �^�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�T�a
echo.
python run.py

pause 