"""
统计分析业务逻辑服务
"""
import json
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import TestTask
from app.models.record import TestRecord
import logging

logger = logging.getLogger(__name__)


class StatisticsService:
    """统计分析服务类"""

    @staticmethod
    def get_statistics_overview(
        db: Session,
        task_id: int = None
    ) -> Dict[str, Any]:
        """
        获取统计概览

        Args:
            db: 数据库会话
            task_id: 任务ID，如果指定则只统计该任务

        Returns:
            统计概览字典
        """
        # 构建查询条件
        query = db.query(TestRecord)
        if task_id:
            query = query.filter(TestRecord.task_id == task_id)

        # 获取所有记录
        records = query.all()

        if not records:
            return {
                "total_comments": 0,
                "total_tags": 0,
                "unique_tags": 0,
                "avg_confidence": 0.0,
                "avg_processing_time": 0.0,
                "top_tags": [],
                "category_distribution": []
            }

        # 基础统计
        total_comments = len(records)
        total_tags = 0
        all_tags = []
        confidences = []
        processing_times = []

        for record in records:
            # 解析标签
            try:
                tags = json.loads(record.tags_json) if isinstance(record.tags_json, str) else record.tags_json
                if isinstance(tags, list):
                    total_tags += len(tags)
                    all_tags.extend(tags)
            except Exception as e:
                logger.error(f"解析标签失败: {e}")

            # 收集置信度和处理时间
            if record.confidence is not None:
                confidences.append(record.confidence)
            if record.processing_time is not None:
                processing_times.append(record.processing_time)

        # 计算平均值
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0

        # 统计标签分布
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 获取Top 10标签
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_tags = [
            {
                "tag": tag,
                "count": count,
                "percentage": round((count / total_comments) * 100, 2) if total_comments > 0 else 0.0
            }
            for tag, count in sorted_tags
        ]

        # 统计分类分布
        category_distribution = StatisticsService._analyze_categories(all_tags, total_comments)

        return {
            "total_comments": total_comments,
            "total_tags": total_tags,
            "unique_tags": len(tag_counts),
            "avg_confidence": round(avg_confidence, 4),
            "avg_processing_time": round(avg_processing_time, 4),
            "top_tags": top_tags,
            "category_distribution": category_distribution
        }

    @staticmethod
    def _analyze_categories(tags: List[str], total_comments: int) -> List[Dict[str, Any]]:
        """
        分析标签分类

        Args:
            tags: 所有标签列表
            total_comments: 总评论数

        Returns:
            分类分布列表
        """
        # 定义分类规则
        categories = {
            "正面情感": ["正面", "积极", "好评", "满意", "喜欢"],
            "负面情感": ["负面", "消极", "差评", "不满意", "不喜欢"],
            "产品性能": ["动力", "油耗", "操控", "舒适", "配置", "性能"],
            "外观设计": ["外观", "内饰", "颜值", "设计", "造型"],
            "空间尺寸": ["空间", "尺寸", "大小", "乘坐", "储物"],
            "价格性价比": ["价格", "性价比", "贵", "便宜", "实惠"],
            "服务售后": ["售后", "服务", "保养", "维修", "质保"],
            "品牌口碑": ["品牌", "口碑", "形象", "知名度"],
            "其他": []
        }

        # 统计每个分类的标签数量
        category_counts = {category: 0 for category in categories.keys()}

        for tag in tags:
            matched = False
            for category, keywords in categories.items():
                if category == "其他":
                    continue
                if any(keyword in tag for keyword in keywords):
                    category_counts[category] += 1
                    matched = True
                    break

            # 如果没有匹配到任何分类，归入"其他"
            if not matched:
                category_counts["其他"] += 1

        # 计算百分比并构建结果
        total_tags = len(tags)
        result = [
            {
                "category": category,
                "count": count,
                "percentage": round((count / total_tags) * 100, 2) if total_tags > 0 else 0.0
            }
            for category, count in category_counts.items()
            if count > 0  # 只返回有数据的分类
        ]

        # 按数量降序排列
        result.sort(key=lambda x: x["count"], reverse=True)

        return result
