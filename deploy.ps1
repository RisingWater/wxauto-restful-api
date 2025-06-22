# wxauto API PowerShell 部署脚本
param(
    [switch]$Force,
    [switch]$SkipService,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
wxauto API 部署脚本

用法:
    .\deploy.ps1 [选项]

选项:
    -Force        强制重新安装，即使已存在
    -SkipService  跳过Windows服务安装
    -Help         显示此帮助信息

示例:
    .\deploy.ps1                    # 正常部署
    .\deploy.ps1 -Force            # 强制重新部署
    .\deploy.ps1 -SkipService      # 仅安装环境，不安装服务
"@
    exit 0
}

# 检查管理员权限
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "错误：需要管理员权限运行此脚本" -ForegroundColor Red
    Write-Host "请右键点击此文件，选择'以管理员身份运行PowerShell'" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "wxauto API PowerShell 部署脚本" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 设置变量
$ServiceName = "wxautoAPI"
$ServiceDisplayName = "wxauto API Service"
$ServiceDescription = "微信自动化API服务"
$AppPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = Join-Path $AppPath ".venv\Scripts\python.exe"
$ScriptPath = Join-Path $AppPath "run.py"

# 检查Python环境
Write-Host "检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python未安装"
    }
    Write-Host "Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：未找到Python，请先安装Python 3.11+" -ForegroundColor Red
    Write-Host "下载地址：https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

# 检查uv包管理器
Write-Host "检查uv包管理器..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "正在安装uv包管理器..." -ForegroundColor Yellow
        Invoke-RestMethod -Uri "https://astral.sh/uv/install.ps1" | Invoke-Expression
        if ($LASTEXITCODE -ne 0) {
            throw "uv安装失败"
        }
    } else {
        Write-Host "uv版本: $uvVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "错误：uv安装失败，请手动安装" -ForegroundColor Red
    Write-Host "安装命令：pip install uv" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

# 创建虚拟环境并安装依赖
Write-Host "正在创建虚拟环境并安装依赖..." -ForegroundColor Yellow
Set-Location $AppPath
uv sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误：依赖安装失败" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 创建必要的目录
Write-Host "创建必要的目录..." -ForegroundColor Yellow
$directories = @("data", "uploads", "wxauto_logs")
foreach ($dir in $directories) {
    $dirPath = Join-Path $AppPath $dir
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        Write-Host "创建目录: $dir" -ForegroundColor Green
    }
}

# 检查配置文件
if (-not (Test-Path (Join-Path $AppPath "config.yaml"))) {
    Write-Host "警告：未找到config.yaml配置文件，将使用默认配置" -ForegroundColor Yellow
} else {
    Write-Host "找到配置文件: config.yaml" -ForegroundColor Green
}

# 测试环境
Write-Host "测试环境..." -ForegroundColor Yellow
try {
    & $PythonPath -c "import fastapi, wxauto; print('环境测试成功！')"
    if ($LASTEXITCODE -ne 0) {
        throw "环境测试失败"
    }
    Write-Host "环境测试成功！" -ForegroundColor Green
} catch {
    Write-Host "错误：环境测试失败" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 安装Windows服务
if (-not $SkipService) {
    Write-Host "安装Windows服务..." -ForegroundColor Yellow
    
    # 检查服务是否存在
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($service) {
        if ($Force) {
            Write-Host "发现现有服务，正在停止并删除..." -ForegroundColor Yellow
            Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            Remove-Service -Name $ServiceName -Force
            Start-Sleep -Seconds 2
        } else {
            Write-Host "服务已存在，使用 -Force 参数强制重新安装" -ForegroundColor Yellow
            Read-Host "按任意键退出"
            exit 1
        }
    }
    
    # 创建服务
    $binPath = "`"$PythonPath`" `"$ScriptPath`""
    New-Service -Name $ServiceName -BinaryPathName $binPath -DisplayName $ServiceDisplayName -StartupType Automatic -Description $ServiceDescription
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "服务创建成功！" -ForegroundColor Green
        
        # 启动服务
        Write-Host "正在启动服务..." -ForegroundColor Yellow
        Start-Service -Name $ServiceName
        Start-Sleep -Seconds 3
        
        # 检查服务状态
        $service = Get-Service -Name $ServiceName
        if ($service.Status -eq "Running") {
            Write-Host "服务启动成功！" -ForegroundColor Green
        } else {
            Write-Host "警告：服务启动失败，请手动检查" -ForegroundColor Yellow
        }
    } else {
        Write-Host "错误：服务创建失败" -ForegroundColor Red
        Read-Host "按任意键退出"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "服务信息：" -ForegroundColor Cyan
Write-Host "  - 服务名称: $ServiceName" -ForegroundColor White
Write-Host "  - 配置文件: config.yaml" -ForegroundColor White
if (-not $SkipService) {
    Write-Host "  - 状态: 自动启动" -ForegroundColor White
}
Write-Host ""
Write-Host "管理命令：" -ForegroundColor Cyan
Write-Host "  - 启动服务: Start-Service $ServiceName" -ForegroundColor White
Write-Host "  - 停止服务: Stop-Service $ServiceName" -ForegroundColor White
Write-Host "  - 重启服务: Restart-Service $ServiceName" -ForegroundColor White
Write-Host "  - 查看状态: Get-Service $ServiceName" -ForegroundColor White
Write-Host "  - 卸载服务: Remove-Service $ServiceName" -ForegroundColor White
Write-Host ""
Write-Host "配置说明：" -ForegroundColor Cyan
Write-Host "  - 服务器端口和配置请编辑 config.yaml 文件" -ForegroundColor White
Write-Host "  - 修改配置后需要重启服务" -ForegroundColor White
Write-Host ""
if (-not $SkipService) {
    Write-Host "服务将在系统启动时自动运行" -ForegroundColor Green
}
Write-Host "如需修改配置，请编辑 config.yaml 文件" -ForegroundColor Yellow
Write-Host ""

Read-Host "按任意键退出" 