@echo off
echo ========================================
echo wxauto API 配置测试脚本
echo ========================================

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo 错误：未找到虚拟环境
    echo 请先运行 setup.bat 安装环境
    pause
    exit /b 1
)

:: 激活虚拟环境并运行配置测试
echo 正在测试配置系统...
call .venv\Scripts\activate.bat
python test_config.py

if %errorLevel% equ 0 (
    echo.
    echo 配置测试通过！
) else (
    echo.
    echo 配置测试失败，请检查错误信息
)

pause 