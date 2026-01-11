"""
数据库初始化脚本
用于创建数据库表和测试数据
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db, SessionLocal
from app.models.task import TestTask
from app.models.record import TestRecord
from app.models.statistic import TagStatistic


def create_test_data():
    """
    创建测试数据
    """
    db = SessionLocal()

    try:
        # 创建测试任务
        test_task = TestTask(
            task_type="single",
            status="completed",
            total_count=1,
            processed_count=1
        )
        db.add(test_task)
        db.flush()  # 获取task_id

        # 创建测试记录
        test_record = TestRecord(
            task_id=test_task.id,
            comment_text="这是一条测试评论",
            tags_json='["测试标签", "正面评价"]',
            confidence=0.95,
            processing_time=1234
        )
        db.add(test_record)

        # 创建测试统计
        test_stat = TagStatistic(
            tag_name="测试标签",
            tag_category="测试",
            occurrence_count=1
        )
        db.add(test_stat)

        db.commit()
        print(f"✅ 测试数据创建成功！")
        print(f"   - 任务ID: {test_task.id}")
        print(f"   - 记录ID: {test_record.id}")
        print(f"   - 统计ID: {test_stat.id}")

        return test_task.id

    except Exception as e:
        db.rollback()
        print(f"❌ 创建测试数据失败: {str(e)}")
        return None
    finally:
        db.close()


def query_test_data():
    """
    查询测试数据
    """
    db = SessionLocal()

    try:
        # 查询任务数量
        task_count = db.query(TestTask).count()
        record_count = db.query(TestRecord).count()
        stat_count = db.query(TagStatistic).count()

        print(f"\n📊 数据库统计:")
        print(f"   - test_tasks表: {task_count} 条记录")
        print(f"   - test_records表: {record_count} 条记录")
        print(f"   - tag_statistics表: {stat_count} 条记录")

        return {
            "tasks": task_count,
            "records": record_count,
            "statistics": stat_count
        }

    except Exception as e:
        print(f"❌ 查询数据失败: {str(e)}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("数据库初始化脚本")
    print("=" * 60)

    # 初始化数据库
    print("\n1. 初始化数据库...")
    init_db()

    # 创建测试数据
    print("\n2. 创建测试数据...")
    task_id = create_test_data()

    # 查询数据
    print("\n3. 查询数据...")
    query_test_data()

    print("\n" + "=" * 60)
    print("✅ 数据库初始化完成！")
    print("=" * 60)
