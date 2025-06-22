#!/usr/bin/env python3
"""
wxauto API 配置测试脚本
测试配置读取功能是否正常工作
"""

import sys
from pathlib import Path
from app.utils.config import settings

def test_config() -> None:
    """测试配置读取功能"""
    print("=" * 50)
    print("wxauto API 配置测试")
    print("=" * 50)
    
    # 测试基本配置读取
    print("测试基本配置读取...")
    
    # 服务器配置
    host = settings.server.host
    port = settings.server.port
    reload = settings.server.reload
    
    print(f"✓ 服务器配置读取成功:")
    print(f"  - 主机: {host}")
    print(f"  - 端口: {port}")
    print(f"  - 热重载: {reload}")
    
    # API配置
    api_prefix = settings.api.prefix
    docs_url = settings.api.docs_url
    
    print(f"✓ API配置读取成功:")
    print(f"  - API前缀: {api_prefix}")
    print(f"  - 文档URL: {docs_url}")
    
    # 数据库配置
    db_type = settings.database.type
    
    print(f"✓ 数据库配置读取成功:")
    print(f"  - 数据库类型: {db_type}")
    
    # 认证配置
    token = settings.auth.token
    
    print(f"✓ 认证配置读取成功:")
    print(f"  - API令牌: {'已设置' if token != 'your-secret-token-here' else '使用默认值'}")
    
    # 测试配置有效性
    print("\n测试配置有效性...")
    
    # 检查端口范围
    if 1 <= port <= 65535:
        print(f"✓ 端口号有效: {port}")
    else:
        print(f"✗ 端口号无效: {port}")
        return False
    
    # 检查主机地址
    if host in ["0.0.0.0", "127.0.0.1", "localhost"] or host.startswith("192.168.") or host.startswith("10."):
        print(f"✓ 主机地址有效: {host}")
    else:
        print(f"⚠ 主机地址可能有问题: {host}")
    
    # 测试URL构建
    base_url = f"http://{host}:{port}"
    docs_full_url = f"{base_url}{docs_url}"
    
    print(f"✓ URL构建测试:")
    print(f"  - 基础URL: {base_url}")
    print(f"  - 文档URL: {docs_full_url}")
    
    print("\n" + "=" * 50)
    print("配置测试完成 - 所有测试通过！")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        success = test_config()
        if success:
            print("\n配置系统工作正常，可以启动服务。")
        else:
            print("\n配置测试失败，请检查配置文件。")
            sys.exit(1)
    except Exception as e:
        print(f"配置测试失败: {e}")
        sys.exit(1) 