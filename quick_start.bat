@echo off
chcp 65001 >nul
echo ========================================
echo wxauto API 快速启动脚本
echo ========================================

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo 错误：未找到虚拟环境
    echo 请先运行 setup.bat 安装环境
    pause
    exit /b 1
)

:: 激活虚拟环境并启动服务
echo 正在启动服务...
call .venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause 