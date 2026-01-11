"""
FastAPI应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="用户画像Agent测试系统API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    """
    # 初始化数据库
    init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动成功！")


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": f"欢迎使用{settings.APP_NAME}",
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "ok"}


# 注册路由
from app.api import test, statistics  # 导入测试路由和统计路由

app.include_router(test.router, prefix="/api/v1/test", tags=["测试"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["统计分析"])

# 后续会添加其他路由
# app.include_router(history.router, prefix="/api/v1/history", tags=["历史记录"])
