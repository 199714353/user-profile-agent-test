"""
标签统计模型
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class TagStatistic(Base):
    """标签统计表"""
    __tablename__ = "tag_statistics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_name = Column(String(100), nullable=False, index=True)
    tag_category = Column(String(50), nullable=True)  # 标签分类(如: '需求', '情感', '场景'等)
    occurrence_count = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
