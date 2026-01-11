"""
统计分析相关的Pydantic schemas
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TagDistributionItem(BaseModel):
    """标签分布项"""
    tag: str = Field(..., description="标签名称")
    count: int = Field(..., description="出现次数")
    percentage: float = Field(..., description="占比（百分比）")


class CategoryDistributionItem(BaseModel):
    """分类分布项"""
    category: str = Field(..., description="分类名称")
    count: int = Field(..., description="出现次数")
    percentage: float = Field(..., description="占比（百分比）")


class StatisticsOverview(BaseModel):
    """统计概览"""
    total_comments: int = Field(..., description="总评论数")
    total_tags: int = Field(..., description="总标签数")
    unique_tags: int = Field(..., description="唯一标签数")
    avg_confidence: float = Field(..., description="平均置信度")
    avg_processing_time: float = Field(..., description="平均处理时间（秒）")
    top_tags: List[TagDistributionItem] = Field(..., description="热门标签Top 10")
    category_distribution: List[CategoryDistributionItem] = Field(
        ..., description="分类分布"
    )


class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str = Field(..., description="错误详情")
