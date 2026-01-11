"""
测试任务模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class TestTask(Base):
    """测试任务表"""
    __tablename__ = "test_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_type = Column(String(20), nullable=False, default="single")  # 'single' 或 'batch'
    status = Column(String(20), nullable=False, default="pending")  # 'pending', 'processing', 'completed', 'failed'
    total_count = Column(Integer, nullable=False, default=0)
    processed_count = Column(Integer, nullable=False, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
