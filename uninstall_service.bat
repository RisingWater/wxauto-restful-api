@echo off
chcp 936 >nul
echo ========================================
echo wxauto API 服务卸载脚本
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

:: 检查服务是否存在
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorLevel% neq 0 (
    echo 服务 %SERVICE_NAME% 不存在，无需卸载
    pause
    exit /b 0
)

:: 停止服务
echo 正在停止服务...
net stop "%SERVICE_NAME%" >nul 2>&1

:: 删除服务
echo 正在删除服务...
sc delete "%SERVICE_NAME%"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo 服务卸载成功！
    echo ========================================
    echo 服务 %SERVICE_NAME% 已被完全移除
    echo.
) else (
    echo.
    echo ========================================
    echo 服务卸载失败！
    echo ========================================
    echo 请检查错误信息并重试
    echo.
)

pause 