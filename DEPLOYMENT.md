# wxauto API 部署指南

## 🎯 推荐部署方案

### 方案一：Windows服务部署（最优雅）

这是推荐的部署方案，将应用注册为Windows服务，实现开机自启动和后台运行。

#### 一键部署
```bash
# 右键点击 deploy.bat，选择"以管理员身份运行"
deploy.bat
```

#### PowerShell部署（功能更强大）
```powershell
# 以管理员身份运行PowerShell
.\deploy.ps1

# 强制重新部署
.\deploy.ps1 -Force

# 仅安装环境，不安装服务
.\deploy.ps1 -SkipService

# 查看帮助
.\deploy.ps1 -Help
```

### 方案二：手动部署

适合开发环境或临时使用。

```bash
# 1. 环境设置
setup.bat

# 2. 启动服务
run.bat
# 或
quick_start.bat
```

## 📋 部署前准备

### 系统要求
- Windows 10/11
- Python 3.11+
- 管理员权限（用于服务安装）

### 软件依赖
- 微信客户端（默认路径：`C:/Program Files/WeChat/WeChat.exe`）
- wxauto库（通过uv自动安装）

## 🚀 部署步骤详解

### 1. 环境设置（setup.bat）
- 检查Python版本
- 安装uv包管理器
- 创建虚拟环境
- 安装项目依赖
- 创建必要目录
- 环境测试

### 2. 服务安装（install_service.bat）
- 检查管理员权限
- 验证环境完整性
- 注册Windows服务
- 设置自动启动
- 启动服务

### 3. 服务管理
```bash
# 启动服务
net start wxautoAPI

# 停止服务
net stop wxautoAPI

# 重启服务
net stop wxautoAPI && net start wxautoAPI

# 查看状态
sc query wxautoAPI
```

## 🔧 配置说明

### 主要配置文件
- `config.yaml` - 主配置文件
- `pyproject.toml` - 项目依赖

### 重要配置项
```yaml
# 服务器配置
server:
  host: "0.0.0.0"
  port: 8000

# 认证配置
auth:
  token: "your-secret-token-here"

# 微信配置
wechat:
  app_path: "C:/Program Files/WeChat/WeChat.exe"
```

## 📊 部署验证

### 1. 服务状态检查
```bash
# 检查服务状态
sc query wxautoAPI

# 检查端口占用
netstat -an | findstr :8000
```

### 2. API访问测试
- 浏览器访问：http://localhost:8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

### 3. 日志检查
- 应用日志：`wxauto_logs/` 目录
- 服务日志：Windows事件查看器

## 🛠️ 故障排除

### 常见问题

#### 1. 权限不足
```
错误：需要管理员权限运行此脚本
```
**解决方案**：右键点击脚本，选择"以管理员身份运行"

#### 2. Python版本不兼容
```
错误：未找到Python，请先安装Python 3.11+
```
**解决方案**：下载并安装Python 3.11+

#### 3. 端口被占用
```
错误：端口8000已被占用
```
**解决方案**：
- 修改 `config.yaml` 中的端口配置
- 或停止占用端口的程序

#### 4. 微信路径错误
```
错误：微信客户端路径不正确
```
**解决方案**：检查并修改 `config.yaml` 中的 `wechat.app_path`

#### 5. 服务启动失败
```
错误：服务启动失败
```
**解决方案**：
1. 检查日志文件
2. 验证配置文件
3. 重新安装服务

### 日志查看

#### 应用日志
```bash
# 查看最新日志
Get-Content wxauto_logs\app_$(Get-Date -Format 'yyyyMMdd').log -Tail 50
```

#### 服务日志
```bash
# 查看Windows服务日志
Get-EventLog -LogName Application -Source "wxautoAPI" -Newest 10
```

## 🔄 更新部署

### 代码更新
```bash
# 1. 拉取最新代码
git pull

# 2. 更新依赖
uv sync

# 3. 重启服务
Restart-Service wxautoAPI
```

### 配置更新
```bash
# 1. 修改 config.yaml
# 2. 重启服务
Restart-Service wxautoAPI
```

## 🗑️ 卸载部署

### 卸载服务
```bash
# 使用脚本卸载
uninstall_service.bat

# 或手动卸载
Remove-Service wxautoAPI
```

### 清理环境
```bash
# 删除虚拟环境
Remove-Item .venv -Recurse -Force

# 删除日志文件
Remove-Item wxauto_logs -Recurse -Force

# 删除数据文件
Remove-Item data -Recurse -Force
```

## 📞 技术支持

如遇到部署问题，请检查：
1. 系统要求是否满足
2. 权限是否足够
3. 配置文件是否正确
4. 日志文件中的错误信息

## 📝 注意事项

- 确保微信客户端已正确安装
- 定期备份配置文件和数据
- 监控服务运行状态
- 及时更新依赖包
- 保护API访问令牌 