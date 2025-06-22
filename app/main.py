from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import wechat, chat, apps, files
from app.utils.auth import get_current_token
from app.models.response import APIResponse
from app.utils.config import settings
from typing import Any, Dict

app = FastAPI(
    title="WXAuto API",
    description="微信自动化API服务",
    version="1.0.0",
    docs_url=settings.api.docs_url,
    redoc_url=settings.api.redoc_url,
    openapi_url=settings.api.openapi_url
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """统一处理HTTP异常
    
    Args:
        request: 请求对象
        exc: HTTP异常
        
    Returns:
        JSONResponse: 统一格式的响应
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            message=exc.detail,
            data=None
        ).model_dump()
    )

@app.get("/")
async def root():
    """根路径
    
    Returns:
        dict: 欢迎信息
    """
    return {"message": "欢迎使用WXAuto API"}

# 注册路由，添加认证依赖
app.include_router(wechat.router, prefix=f"{settings.api.prefix}/wechat", tags=["WeChat"], dependencies=[Depends(get_current_token)])
app.include_router(chat.router, prefix=f"{settings.api.prefix}/chat", tags=["Chat"], dependencies=[Depends(get_current_token)])
app.include_router(apps.router, prefix=f"{settings.api.prefix}/apps", tags=["Apps"], dependencies=[Depends(get_current_token)])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])




