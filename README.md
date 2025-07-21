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
- **支持wxauto和wxautox两个版本**

## 包版本支持

本项目支持同时使用 `wxauto`（开源免费版）和 `wxautox`（闭源收费版）两个版本：

| 功能 | wxauto | wxautox |
|------|--------|---------|
| 基础消息发送 | ✅ | ✅ |
| 文件发送 | ✅ | ✅ |
| 聊天窗口切换 | ✅ | ✅ |
| 获取子窗口 | ✅ | ✅ |
| 获取消息 | ✅ | ✅ |
| 监听聊天 | ✅ | ✅ |
| 获取新消息 | ✅ | ✅ |
| 引用消息 | ✅ | ✅ |
| URL卡片发送 | ❌ | ✅ |
| 好友申请管理 | ❌ | ✅ |
| 页面切换 | ❌ | ✅ |


## 项目结构

```
wxauto-restful-api/
├── app/                    # 主应用目录
│   ├── api/               # API路由
│   │   └── v1/           # API版本1
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   │   ├── wx_package_manager.py  # wx包管理器
│   │   └── route_condition.py     # 条件路由装饰器
│   └── run.py            # 启动脚本
├── config.yaml           # 主配置文件
├── check_config.py       # 配置检查脚本
├── WX_PACKAGE_GUIDE.md   # 包配置指南
└── schemas.json          # API模式定义
```

### 安装对应包

```bash
# 使用 wxauto
pip install wxauto

# 或使用 wxautox
pip install wxautox
```

> [!NOTE]
> wxautox为Plus版本，具体可了解[Plus版本](https://plus.wxauto.org/plus)

## 配置管理

### 配置文件
项目使用 `config.yaml` 作为主配置文件，所有服务器设置都通过此文件管理：

```yaml
package: "wxauto"  # 指定使用的包版本

server:
  host: "0.0.0.0"  # 服务器监听地址
  port: 8000       # 服务器监听端口
  reload: true     # 是否启用热重载
```

### 修改配置
1. 编辑 `config.yaml` 文件
2. 修改所需的配置项（如端口号、包版本）
3. 重启服务使配置生效

### 手动模式
```bash
# 启动服务（使用配置文件中的设置）
run.bat

# 或手动启动
python run.py
```

### Dify调用wxauto

1. 修改`schemas.json`中的servers - url中的服务地址，改为你的实际地址
2. Dify添加自定义工具，将`schemas.json`输入自定义工具

## API文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**注意**：实际端口号请查看 `config.yaml` 中的 `server.port` 设置

## API接口

### 基础接口（两个版本都支持）

- `POST /v1/wechat/send` - 发送消息
- `POST /v1/wechat/sendfile` - 发送文件
- `POST /v1/wechat/chatwith` - 切换聊天窗口
- `POST /v1/wechat/getallsubwindow` - 获取所有子窗口
- `POST /v1/wechat/getallmessage` - 获取所有消息
- `POST /v1/wechat/addlistenchat` - 添加监听聊天
- `POST /v1/wechat/getnextnewmessage` - 获取下一个新消息

### wxautox特有接口

- `POST /v1/wechat/sendurlcard` - 发送URL卡片
- `POST /v1/wechat/getnewfriends` - 获取好友申请
- `POST /v1/wechat/newfriend/accept` - 接受好友申请
- `POST /v1/wechat/switch/chat` - 切换到聊天页面

### 信息接口

- `GET /v1/info/package` - 获取包信息
- `GET /v1/info/features` - 获取支持功能
- `GET /v1/info/status` - 获取服务状态

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
- `config.yaml` - 主配置文件（包含所有服务器设置和包版本）
- `pyproject.toml` - 项目依赖配置

### 重要配置项
- `package` - 指定使用的包版本（wxauto/wxautox）
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
- **动态包导入系统**
- **条件路由系统**

## 注意事项

- 请确保wxauto已正确安装并配置
- 建议在开发环境中使用
- 注意保护API访问token
- 定期检查日志文件
- 服务部署需要管理员权限
- **重要**：所有端口配置都通过 `config.yaml` 文件管理，批处理脚本不再硬编码端口
- **包版本兼容性**：确保安装的包版本与代码兼容
- **功能差异**：注意两个版本的功能差异

## 许可证

MIT License
