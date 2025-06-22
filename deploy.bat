@echo off
chcp 936 >nul
echo ========================================
echo wxauto API 一键部署脚本
echo ========================================

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误：需要管理员权限运行此脚本
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 步骤1: 环境设置...
call setup.bat
if %errorLevel% neq 0 (
    echo 环境设置失败，部署终止
    pause
    exit /b 1
)

echo.
echo 步骤2: 安装Windows服务...
call install_service.bat
if %errorLevel% neq 0 (
    echo 服务安装失败，部署终止
    pause
    exit /b 1
)

echo.
echo ========================================
echo 一键部署完成！
echo ========================================
echo.
echo 服务信息：
echo   - 服务名称: wxautoAPI
echo   - 配置文件: config.yaml
echo   - 状态: 自动启动
echo.
echo 管理命令：
echo   - 启动服务: net start wxautoAPI
echo   - 停止服务: net stop wxautoAPI
echo   - 重启服务: net stop wxautoAPI && net start wxautoAPI
echo   - 卸载服务: uninstall_service.bat
echo.
echo 配置说明：
echo   - 服务器端口和配置请编辑 config.yaml 文件
echo   - 修改配置后需要重启服务
echo.
echo 服务将在系统启动时自动运行
echo 如需修改配置，请编辑 config.yaml 文件
echo.

pause 