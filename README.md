# wxauto API

这是一个基于FastAPI开发的HTTP API服务，用于适配wxauto的自动化操作。该服务提供了微信自动化操作的RESTful API接口，支持消息发送、群管理、好友管理等功能。

## 功能特性

- 微信消息发送与接收
- 群聊管理
- 好友管理
- 应用管理
- 统一的认证机制
- 标准化的API响应格式
- 灵活的配置管理

## 项目结构

```
wxauto-restful-api/
├── app/                    # 主应用目录
│   ├── api/               # API路由
│   │   └── v1/           # API版本1
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   └── run.py            # 启动脚本
├── config.yaml           # 主配置文件
├── check_config.py       # 配置检查脚本
└── schemas.json          # API模式定义
```

## 🚀 一键部署（推荐）

### Windows服务部署（最优雅）

1. **一键部署**（推荐）：
   ```bash
   # 右键点击 deploy.bat，选择"以管理员身份运行"
   deploy.bat
   ```

2. **分步部署**：
   ```bash
   # 步骤1：环境设置
   setup.bat
   
   # 步骤2：安装Windows服务（需要管理员权限）
   install_service.bat
   ```

### 手动部署

1. 确保已安装Python 3.11+
2. 克隆项目仓库
3. 运行环境设置：
   ```bash
   setup.bat
   ```
4. 启动服务：
   ```bash
   quick_start.bat
   ```

## 配置管理

### 配置文件
项目使用 `config.yaml` 作为主配置文件，所有服务器设置都通过此文件管理：

```yaml
server:
  host: "0.0.0.0"  # 服务器监听地址
  port: 8000       # 服务器监听端口
  reload: true     # 是否启用热重载
```

### 配置检查
运行配置检查脚本查看当前配置：
```bash
check_config.bat
```

### 修改配置
1. 编辑 `config.yaml` 文件
2. 修改所需的配置项（如端口号）
3. 重启服务使配置生效

## 服务管理

### Windows服务模式
```bash
# 启动服务
net start wxautoAPI

# 停止服务
net stop wxautoAPI

# 重启服务
net stop wxautoAPI && net start wxautoAPI

# 卸载服务
uninstall_service.bat
```

### 手动模式
```bash
# 启动服务（使用配置文件中的设置）
quick_start.bat

# 或手动启动
python run.py
```

### 对接Dify

1. 修改`schemas.json`中的servers - url中的服务地址，改为你的实际地址

## API文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**注意**：实际端口号请查看 `config.yaml` 中的 `server.port` 设置

## API端点

### 微信相关接口 (/v1/wechat)
- 消息发送
- 群聊管理
- 好友管理

### 聊天相关接口 (/v1/chat)
- 消息处理
- 会话管理

### 应用相关接口 (/v1/apps)
- 应用管理
- 配置管理

## 认证

所有API请求都需要在Header中包含有效的认证token：
```
Authorization: Bearer <your-token>
```

## 响应格式

所有API响应都遵循统一的格式：
```json
{
    "success": true,
    "message": "操作成功",
    "data": {}
}
```

## 配置说明

### 主要配置文件
- `config.yaml` - 主配置文件（包含所有服务器设置）
- `pyproject.toml` - 项目依赖配置

### 重要配置项
- `server.port` - 服务端口（默认8000）
- `server.host` - 服务器监听地址（默认0.0.0.0）
- `server.reload` - 热重载开关（默认true）
- `auth.token` - API访问令牌
- `wechat.app_path` - 微信安装路径
- `database.type` - 数据库类型（默认sqlite）

### 配置优先级
1. `config.yaml` 文件中的设置
2. 代码中的默认值

## 开发说明

- 使用FastAPI框架开发
- 采用模块化设计
- 包含完整的类型注解
- 统一的错误处理机制
- 详细的API文档
- 灵活的配置管理

## 注意事项

- 请确保wxauto已正确安装并配置
- 建议在开发环境中使用
- 注意保护API访问token
- 定期检查日志文件
- 服务部署需要管理员权限
- **重要**：所有端口配置都通过 `config.yaml` 文件管理，批处理脚本不再硬编码端口

## 故障排除

### 常见问题
1. **权限不足**：确保以管理员身份运行部署脚本
2. **Python版本**：确保使用Python 3.11+
3. **端口占用**：检查config.yaml中设置的端口是否被占用
4. **微信路径**：确认config.yaml中的微信安装路径正确
5. **配置问题**：运行 `check_config.bat` 检查配置

### 日志查看
- 应用日志：`wxauto_logs/` 目录
- 服务日志：Windows事件查看器

### 配置验证
```bash
# 检查当前配置
check_config.bat

# 查看配置详情
python check_config.py
```

## 许可证

MIT License
