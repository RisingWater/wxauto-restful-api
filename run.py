#!/usr/bin/env python3
"""
wxauto API 启动脚本
从配置文件读取服务器配置并启动服务
"""

import sys
import uvicorn
import webbrowser
from pathlib import Path
from app.utils.config import settings
from app.utils.logger import setup_logger

# 延迟打开浏览器
def open_browser(url):
    import time
    time.sleep(2)
    webbrowser.open(url)

def main() -> None:
    """主函数，启动FastAPI应用
    
    从config.yaml读取服务器配置，包括host和port
    """
    # 设置日志
    logger = setup_logger()
    
    # 获取服务器配置
    host = settings.server.host
    port = settings.server.port
    reload = settings.server.reload
    url = f"http://127.0.0.1:{port}{settings.api.docs_url}"

    logger.info(f"启动wxauto API服务")
    logger.info(f"服务器地址: 127.0.0.1:{port}")
    logger.info(f"热重载: {'启用' if reload else '禁用'}")
    logger.info(f"API文档: {url}")
    
    try:
        import threading
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
        # 启动uvicorn服务器
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=settings.logging.level.lower()
        )
    except KeyboardInterrupt:
        logger.info("服务已停止")
    except Exception as e:
        logger.error(f"启动服务失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 