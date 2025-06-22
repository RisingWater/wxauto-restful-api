@echo off

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo    ╔══════════════════════════════════════════════════════════════╗
    echo    ║                        错误信息                               ║
    echo    ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo    错误：未找到虚拟环境
    echo    请先运行 setup.bat 安装环境
    echo.
    pause
    exit /b 1
)

:: 检查配置文件
if not exist "config.yaml" (
    echo    ╔══════════════════════════════════════════════════════════════╗
    echo    ║                        警告信息                               ║
    echo    ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo    警告：未找到config.yaml配置文件，将使用默认配置
    echo.
)

:: 激活虚拟环境并启动服务
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                        启动信息                               ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
echo    正在启动服务...
echo    将从config.yaml读取服务器配置...
echo.
call .venv\Scripts\activate.bat
echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                    wxauto API 快速启动脚本                    ║
echo    ║                                                              ║
echo    ║   ██╗    ██╗██╗  ██╗ █████╗ ██╗   ██╗████████╗ ██████╗       ║
echo    ║   ██║    ██║╚██╗██╔╝██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗      ║
echo    ║   ██║ █╗ ██║ ╚███╔╝ ███████║██║   ██║   ██║   ██║   ██║      ║
echo    ║   ██║███╗██║ ██╔██╗ ██╔══██║██║   ██║   ██║   ██║   ██║      ║
echo    ║   ╚███╔███╔╝██╔╝ ██╗██║  ██║╚██████╔╝   ██║   ╚██████╔╝      ║
echo    ║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝       ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
python run.py

pause 