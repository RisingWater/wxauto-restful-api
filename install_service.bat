@echo off
echo ========================================
echo wxauto API 服务安装脚本
echo ========================================

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误：需要管理员权限运行此脚本
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 设置变量
set SERVICE_NAME=wxautoAPI
set SERVICE_DISPLAY_NAME=wxauto API Service
set SERVICE_DESCRIPTION=微信自动化API服务
set APP_PATH=%~dp0
set PYTHON_PATH=%APP_PATH%.venv\Scripts\python.exe
set SCRIPT_PATH=%APP_PATH%\run.py

:: 检查Python环境
if not exist "%PYTHON_PATH%" (
    echo 错误：未找到Python虚拟环境
    echo 请先运行 setup.bat 安装依赖
    pause
    exit /b 1
)

:: 检查主程序
if not exist "%SCRIPT_PATH%" (
    echo 错误：未找到主程序文件
    pause
    exit /b 1
)

:: 检查配置文件
if not exist "%APP_PATH%config.yaml" (
    echo 警告：未找到config.yaml配置文件，将使用默认配置
)

:: 停止并删除已存在的服务
echo 检查现有服务...
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorLevel% equ 0 (
    echo 发现现有服务，正在停止...
    net stop "%SERVICE_NAME%" >nul 2>&1
    echo 正在删除现有服务...
    sc delete "%SERVICE_NAME%" >nul 2>&1
    timeout /t 2 >nul
)

:: 创建服务
echo 正在创建Windows服务...
echo 服务将从config.yaml读取配置...
sc create "%SERVICE_NAME%" binPath= "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" DisplayName= "%SERVICE_DISPLAY_NAME%" start= auto

:: 设置服务描述
sc description "%SERVICE_NAME%" "%SERVICE_DESCRIPTION%"

:: 启动服务
echo 正在启动服务...
net start "%SERVICE_NAME%"

:: 检查服务状态
sc query "%SERVICE_NAME%" | find "RUNNING" >nul
if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo 服务安装成功！
    echo ========================================
    echo 服务名称: %SERVICE_NAME%
    echo 显示名称: %SERVICE_DISPLAY_NAME%
    echo 配置文件: config.yaml
    echo.
    echo 服务管理命令：
    echo   启动服务: net start %SERVICE_NAME%
    echo   停止服务: net stop %SERVICE_NAME%
    echo   重启服务: net stop %SERVICE_NAME% && net start %SERVICE_NAME%
    echo   删除服务: sc delete %SERVICE_NAME%
    echo.
    echo 注意：服务端口和配置请查看config.yaml文件
    echo.
) else (
    echo.
    echo ========================================
    echo 服务安装失败！
    echo ========================================
    echo 请检查错误信息并重试
    echo.
)

pause 