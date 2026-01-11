"""
测试记录模型
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class TestRecord(Base):
    """测试记录表"""
    __tablename__ = "test_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("test_tasks.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    tags_json = Column(Text, nullable=False)  # JSON格式存储标签
    confidence = Column(Float, nullable=True)  # 置信度
    processing_time = Column(Float, nullable=True)  # 处理耗时(毫秒)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
