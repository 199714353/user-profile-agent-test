"""
统计分析相关的API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.database import get_db
from app.schemas.statistics import StatisticsOverview, ErrorResponse
from app.services.stats_service import StatisticsService

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()


@router.get(
    "/overview",
    response_model=StatisticsOverview,
    responses={
        200: {"description": "查询成功"},
        404: {"description": "任务不存在"},
        500: {"model": ErrorResponse, "description": "服务器内部错误"}
    },
    summary="获取统计概览",
    description="获取标签统计分析数据，包括标签分布、分类统计等"
)
async def get_statistics_overview(
    task_id: int = Query(None, description="任务ID，不指定则统计所有任务"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取统计概览接口

    Args:
        task_id: 可选的任务ID
        db: 数据库会话

    Returns:
        统计概览字典

    Raises:
        HTTPException: 任务不存在时抛出
    """
    try:
        # 如果指定了task_id，验证任务是否存在
        if task_id:
            from app.models.task import TestTask
            task = db.query(TestTask).filter(TestTask.id == task_id).first()
            if not task:
                raise HTTPException(
                    status_code=404,
                    detail=f"任务不存在: {task_id}"
                )

        # 获取统计数据
        statistics = StatisticsService.get_statistics_overview(db, task_id)

        logger.info(f"统计查询成功，task_id={task_id}")

        return statistics

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"统计查询失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"统计查询失败: {str(e)}"
        )
