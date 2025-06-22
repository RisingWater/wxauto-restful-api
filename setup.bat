@echo off
chcp 65001 >nul
echo ========================================
echo wxauto API 环境设置脚本
echo ========================================

:: 检查Python版本
echo 检查Python环境...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误：未找到Python，请先安装Python 3.11+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查uv是否安装
echo 检查uv包管理器...
uv --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 正在安装uv包管理器...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if %errorLevel% neq 0 (
        echo 错误：uv安装失败，请手动安装
        echo 安装命令：pip install uv
        pause
        exit /b 1
    )
)

:: 创建虚拟环境并安装依赖
echo 正在创建虚拟环境并安装依赖...
uv sync

if %errorLevel% neq 0 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)

:: 创建必要的目录
echo 创建必要的目录...
if not exist "data" mkdir data
if not exist "uploads" mkdir uploads
if not exist "wxauto_logs" mkdir wxauto_logs

:: 检查配置文件
if not exist "config.yaml" (
    echo 警告：未找到config.yaml配置文件
    echo 将使用默认配置
)

:: 激活虚拟环境并测试
echo 测试环境...
call .venv\Scripts\activate.bat
python -c "import fastapi, wxautox; print('环境测试成功！')"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo 环境设置完成！
    echo ========================================
    echo 现在可以运行以下命令：
    echo   启动服务: run.bat
    echo   安装为Windows服务: install_service.bat (需要管理员权限)
    echo.
) else (
    echo.
    echo ========================================
    echo 环境设置失败！
    echo ========================================
    echo 请检查错误信息并重试
    echo.
)

pause 