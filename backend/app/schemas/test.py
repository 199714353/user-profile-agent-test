"""
测试相关的Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Request schemas
class SingleTestRequest(BaseModel):
    """单条测试请求"""
    comment: str = Field(..., min_length=1, max_length=5000, description="用户评论文本")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "这款车的动力太棒了，加速响应非常快！"
            }
        }


# Response schemas
class TagResult(BaseModel):
    """标签结果"""
    tags: List[str] = Field(description="提取的标签列表")
    confidence: float = Field(default=0.0, description="置信度")
    processing_time: float = Field(description="处理时间（毫秒）")


class SingleTestResponse(BaseModel):
    """单条测试响应"""
    task_id: int = Field(description="任务ID")
    status: str = Field(description="任务状态")
    result: Optional[TagResult] = Field(None, description="标签结果")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "status": "completed",
                "result": {
                    "tags": ["动力性能:正面", "动力性能", "正面"],
                    "confidence": 0.0,
                    "processing_time": 4500.0
                }
            }
        }


class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    task_type: str
    status: str
    total_count: int
    processed_count: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecordResponse(BaseModel):
    """测试记录响应"""
    id: int
    task_id: int
    comment_text: str
    tags_json: str
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Error response schema
class ErrorResponse(BaseModel):
    """错误响应"""
    error: str = Field(description="错误信息")
    detail: Optional[str] = Field(None, description="详细错误信息")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid input",
                "detail": "评论内容不能为空"
            }
        }


# Batch test schemas
class BatchUploadResponse(BaseModel):
    """批量上传响应"""
    task_id: int = Field(description="任务ID")
    status: str = Field(description="任务状态")
    total_count: int = Field(description="总评论数")
    message: str = Field(description="提示信息")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 10,
                "status": "processing",
                "total_count": 100,
                "message": "批量任务已创建，正在处理中"
            }
        }


class BatchProgressResponse(BaseModel):
    """批量进度响应"""
    task_id: int
    status: str
    total_count: int
    processed_count: int
    progress: float = Field(description="进度百分比（0-100）")
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
