"""
测试相关的API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.database import get_db
from app.schemas.test import (
    SingleTestRequest,
    SingleTestResponse,
    ErrorResponse,
    BatchUploadResponse,
    BatchProgressResponse
)
from app.services.test_service import TestService
from app.services.batch_test_service import BatchTestService
from app.services.dify_client import DifyClientError

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()


@router.post(
    "/single",
    response_model=SingleTestResponse,
    responses={
        200: {"description": "测试成功"},
        400: {"model": ErrorResponse, "description": "请求参数错误"},
        500: {"model": ErrorResponse, "description": "服务器内部错误"}
    },
    summary="单条评论测试",
    description="对单条用户评论进行标签提取和分析"
)
async def test_single_comment(
    request: SingleTestRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    单条评论测试接口

    Args:
        request: 包含评论内容的请求体
        db: 数据库会话

    Returns:
        包含任务ID和标签结果的响应

    Raises:
        HTTPException: 请求参数错误或服务器内部错误时抛出
    """
    try:
        # 验证评论内容
        comment = request.comment.strip()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="评论内容不能为空"
            )

        if len(comment) > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="评论内容长度不能超过5000个字符"
            )

        # 调用测试服务
        result = await TestService.create_single_test(db, comment)

        return result

    except DifyClientError as e:
        # Dify API调用错误
        logger.error(f"Dify API错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"标签提取失败: {str(e)}"
        )

    except ValueError as e:
        # 业务逻辑错误
        logger.error(f"业务逻辑错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        # 未预期的错误
        logger.error(f"未预期的错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {str(e)}"
        )


@router.get(
    "/task/{task_id}",
    responses={
        200: {"description": "获取成功"},
        404: {"description": "任务不存在"}
    },
    summary="获取任务详情",
    description="根据任务ID获取测试任务详情和结果"
)
async def get_task_detail(
    task_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取任务详情接口

    Args:
        task_id: 任务ID
        db: 数据库会话

    Returns:
        任务详情字典

    Raises:
        HTTPException: 任务不存在时抛出
    """
    try:
        result = TestService.get_task(db, task_id)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:
        logger.error(f"获取任务详情失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取任务详情失败: {str(e)}"
        )


@router.post(
    "/batch/upload",
    response_model=BatchUploadResponse,
    responses={
        200: {"description": "上传成功"},
        400: {"model": ErrorResponse, "description": "文件格式错误"},
        500: {"model": ErrorResponse, "description": "服务器内部错误"}
    },
    summary="批量测试上传",
    description="上传CSV文件进行批量评论测试"
)
async def upload_batch_test(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="CSV文件"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    批量测试上传接口

    Args:
        background_tasks: FastAPI后台任务
        file: 上传的CSV文件
        db: 数据库会话

    Returns:
        包含任务ID的响应
    """
    try:
        # 读取文件内容
        file_content = await file.read()
        filename = file.filename

        # 解析CSV文件
        try:
            comments, file_info = BatchTestService.parse_csv_file(
                file_content,
                filename
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        # 创建批量任务
        task_id = await BatchTestService.create_batch_task(db, comments)

        # 启动后台任务处理
        background_tasks.add_task(
            process_batch_comments,
            task_id,
            comments
        )

        logger.info(f"批量任务创建成功，task_id={task_id}, 评论数={len(comments)}")

        return {
            "task_id": task_id,
            "status": "processing",
            "total_count": len(comments),
            "message": f"批量任务已创建，正在处理{len(comments)}条评论"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"批量上传失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量上传失败: {str(e)}"
        )


@router.get(
    "/batch/progress/{task_id}",
    response_model=BatchProgressResponse,
    responses={
        200: {"description": "查询成功"},
        404: {"description": "任务不存在"}
    },
    summary="查询批量任务进度",
    description="查询批量测试任务的实时进度"
)
async def get_batch_progress(
    task_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    批量进度查询接口

    Args:
        task_id: 任务ID
        db: 数据库会话

    Returns:
        进度信息字典

    Raises:
        HTTPException: 任务不存在时抛出
    """
    try:
        progress = BatchTestService.get_batch_progress(db, task_id)
        return progress

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:
        logger.error(f"查询进度失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询进度失败: {str(e)}"
        )


# 后台任务处理函数
async def process_batch_comments(task_id: int, comments: list[str]):
    """
    后台任务：处理批量评论

    Args:
        task_id: 任务ID
        comments: 评论列表
    """
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        await BatchTestService.process_batch_task(db, task_id, comments)
    finally:
        db.close()
