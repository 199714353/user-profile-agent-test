"""
批量测试业务逻辑服务
"""
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.task import TestTask
from app.models.record import TestRecord
from app.services.dify_client import dify_client, DifyClientError
from app.utils.csv_parser import CSVParser
import logging

logger = logging.getLogger(__name__)


class BatchTestService:
    """批量测试服务类"""

    @staticmethod
    async def create_batch_task(
        db: Session,
        comments: List[str]
    ) -> int:
        """
        创建批量测试任务

        Args:
            db: 数据库会话
            comments: 评论列表

        Returns:
            任务ID
        """
        # 创建批量任务
        task = TestTask(
            task_type="batch",
            status="pending",
            total_count=len(comments),
            processed_count=0
        )
        db.add(task)
        db.commit()

        logger.info(f"批量任务创建成功，task_id={task.id}, 总数={len(comments)}")

        return task.id

    @staticmethod
    async def process_batch_task(
        db: Session,
        task_id: int,
        comments: List[str]
    ):
        """
        处理批量任务（后台任务）

        Args:
            db: 数据库会话
            task_id: 任务ID
            comments: 评论列表
        """
        task = db.query(TestTask).filter(TestTask.id == task_id).first()
        if not task:
            logger.error(f"任务不存在: {task_id}")
            return

        try:
            # 更新任务状态为处理中
            task.status = "processing"
            db.commit()

            logger.info(f"开始处理批量任务，task_id={task_id}, 评论数={len(comments)}")

            # 处理每条评论
            for idx, comment in enumerate(comments):
                try:
                    logger.info(f"处理第{idx + 1}/{len(comments)}条评论，task_id={task_id}")

                    # 调用Dify API
                    dify_result = await dify_client.get_comment_tags(comment)

                    # 保存结果
                    record = TestRecord(
                        task_id=task.id,
                        comment_text=comment,
                        tags_json=json.dumps(dify_result['tags'], ensure_ascii=False),
                        confidence=dify_result.get('confidence', 0.0),
                        processing_time=dify_result.get('processing_time', 0.0)
                    )
                    db.add(record)

                    # 更新进度
                    task.processed_count += 1
                    db.commit()

                    logger.info(f"第{idx + 1}条评论处理成功，task_id={task_id}")

                except DifyClientError as e:
                    logger.error(f"第{idx + 1}条评论处理失败: {str(e)}")
                    # 保存失败记录
                    record = TestRecord(
                        task_id=task.id,
                        comment_text=comment,
                        tags_json=json.dumps(['处理失败'], ensure_ascii=False),
                        confidence=0.0,
                        processing_time=0.0
                    )
                    db.add(record)
                    task.processed_count += 1
                    db.commit()

            # 更新任务状态为完成
            task.status = "completed"
            task.completed_at = datetime.now()
            db.commit()

            logger.info(f"批量任务处理完成，task_id={task_id}")

        except Exception as e:
            logger.error(f"批量任务处理失败，task_id={task_id}, error={str(e)}")

            # 更新任务状态为失败
            task.status = "failed"
            task.error_message = str(e)
            db.commit()

    @staticmethod
    def get_batch_progress(
        db: Session,
        task_id: int
    ) -> Dict[str, Any]:
        """
        获取批量任务进度

        Args:
            db: 数据库会话
            task_id: 任务ID

        Returns:
            进度信息字典
        """
        task = db.query(TestTask).filter(TestTask.id == task_id).first()
        if not task:
            raise ValueError(f"任务不存在: {task_id}")

        # 计算进度
        progress = 0.0
        if task.total_count > 0:
            progress = (task.processed_count / task.total_count) * 100

        return {
            "task_id": task.id,
            "status": task.status,
            "total_count": task.total_count,
            "processed_count": task.processed_count,
            "progress": round(progress, 2),
            "error_message": task.error_message
        }

    @staticmethod
    def parse_csv_file(file_content: bytes, filename: str) -> Tuple[List[str], Dict]:
        """
        解析CSV文件

        Args:
            file_content: 文件内容
            filename: 文件名

        Returns:
            (评论列表, 文件信息)
        """
        return CSVParser.parse_csv_file(file_content, filename)
