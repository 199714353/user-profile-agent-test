"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    APP_NAME: str = "用户画像Agent测试系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./user_profile_agent.db"

    # Dify API配置
    DIFY_API_KEY: str = "app-33QFU9RLluraZy9P92lDGjHc"
    DIFY_BASE_URL: str = "https://api.dify.ai/v1"

    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
