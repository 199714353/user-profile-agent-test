"""
测试业务逻辑服务
"""
import json
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.task import TestTask
from app.models.record import TestRecord
from app.services.dify_client import dify_client, DifyClientError
import logging

logger = logging.getLogger(__name__)


class TestService:
    """测试服务类"""

    @staticmethod
    async def create_single_test(
        db: Session,
        comment: str
    ) -> Dict[str, Any]:
        """
        创建并执行单条评论测试

        Args:
            db: 数据库会话
            comment: 用户评论文本

        Returns:
            包含任务ID和结果的字典

        Raises:
            DifyClientError: Dify API调用失败时抛出
        """
        # 1. 创建测试任务记录
        task = TestTask(
            task_type="single",
            status="processing",
            total_count=1,
            processed_count=0
        )
        db.add(task)
        db.flush()  # 获取task_id

        try:
            # 2. 调用Dify API获取标签
            logger.info(f"开始处理单条测试，task_id={task.id}")
            dify_result = await dify_client.get_comment_tags(comment)

            # 3. 创建测试记录
            record = TestRecord(
                task_id=task.id,
                comment_text=comment,
                tags_json=json.dumps(dify_result['tags'], ensure_ascii=False),
                confidence=dify_result.get('confidence', 0.0),
                processing_time=dify_result.get('processing_time', 0.0)
            )
            db.add(record)

            # 4. 更新任务状态
            task.status = "completed"
            task.processed_count = 1
            task.completed_at = datetime.now()

            db.commit()

            logger.info(f"单条测试完成，task_id={task.id}, tags={dify_result['tags']}")

            return {
                "task_id": task.id,
                "status": "completed",
                "result": dify_result
            }

        except DifyClientError as e:
            # 标记任务失败
            task.status = "failed"
            task.error_message = str(e)
            db.commit()

            logger.error(f"单条测试失败，task_id={task.id}, error={str(e)}")
            raise

        except Exception as e:
            # 回滚并标记任务失败
            db.rollback()

            # 重新查询task对象
            task = db.query(TestTask).filter(TestTask.id == task.id).first()
            if task:
                task.status = "failed"
                task.error_message = f"系统错误: {str(e)}"
                db.commit()

            logger.error(f"单条测试系统错误，task_id={task.id}, error={str(e)}")
            raise

    @staticmethod
    def get_task(db: Session, task_id: int) -> Dict[str, Any]:
        """
        获取任务详情

        Args:
            db: 数据库会话
            task_id: 任务ID

        Returns:
            任务详情字典
        """
        task = db.query(TestTask).filter(TestTask.id == task_id).first()
        if not task:
            raise ValueError(f"任务不存在: {task_id}")

        # 获取关联的测试记录
        records = db.query(TestRecord).filter(TestRecord.task_id == task_id).all()

        return {
            "task": {
                "id": task.id,
                "task_type": task.task_type,
                "status": task.status,
                "total_count": task.total_count,
                "processed_count": task.processed_count,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "error_message": task.error_message
            },
            "records": [
                {
                    "id": record.id,
                    "comment_text": record.comment_text,
                    "tags": json.loads(record.tags_json),
                    "confidence": record.confidence,
                    "processing_time": record.processing_time,
                    "created_at": record.created_at.isoformat() if record.created_at else None
                }
                for record in records
            ]
        }
