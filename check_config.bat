@echo off
echo ========================================
echo wxauto API 配置检查脚本
echo ========================================

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo 错误：未找到虚拟环境
    echo 请先运行 setup.bat 安装环境
    pause
    exit /b 1
)

:: 激活虚拟环境并运行配置检查
echo 正在检查配置...
call .venv\Scripts\activate.bat
python check_config.py

pause 