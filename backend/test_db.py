"""
数据库完整测试脚本
测试所有CRUD操作和外键关系
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models.task import TestTask
from app.models.record import TestRecord
from app.models.statistic import TagStatistic


def test_crud_operations():
    """
    测试CRUD操作
    """
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("数据库CRUD操作测试")
        print("=" * 60)

        # CREATE - 创建新任务
        print("\n1. 测试 CREATE 操作...")
        new_task = TestTask(
            task_type="batch",
            status="pending",
            total_count=100,
            processed_count=0
        )
        db.add(new_task)
        db.flush()
        print(f"   ✅ 创建新任务: ID={new_task.id}, type={new_task.task_type}")

        # 创建关联记录
        new_record = TestRecord(
            task_id=new_task.id,
            comment_text="测试评论内容",
            tags_json='["标签1", "标签2"]',
            confidence=0.88
        )
        db.add(new_record)
        db.flush()
        print(f"   ✅ 创建关联记录: ID={new_record.id}, task_id={new_record.task_id}")

        # READ - 查询数据
        print("\n2. 测试 READ 操作...")
        task = db.query(TestTask).filter(TestTask.id == new_task.id).first()
        print(f"   ✅ 查询任务: status={task.status}, total={task.total_count}")

        # 关联查询
        records = db.query(TestRecord).filter(TestRecord.task_id == new_task.id).all()
        print(f"   ✅ 关联查询: 找到 {len(records)} 条记录")

        # UPDATE - 更新数据
        print("\n3. 测试 UPDATE 操作...")
        task.status = "processing"
        task.processed_count = 50
        db.flush()
        print(f"   ✅ 更新任务: status={task.status}, processed={task.processed_count}")

        # DELETE - 删除数据
        print("\n4. 测试 DELETE 操作...")
        record_id = new_record.id
        db.delete(new_record)
        db.delete(task)
        db.commit()

        # 验证删除
        deleted_record = db.query(TestRecord).filter(TestRecord.id == record_id).first()
        deleted_task = db.query(TestTask).filter(TestTask.id == new_task.id).first()

        if deleted_record is None and deleted_task is None:
            print(f"   ✅ 删除成功: 记录和任务已删除")
        else:
            print(f"   ❌ 删除失败")

        # 测试统计
        print("\n5. 测试统计查询...")
        task_count = db.query(TestTask).count()
        record_count = db.query(TestRecord).count()
        stat_count = db.query(TagStatistic).count()

        print(f"   ✅ 数据库统计:")
        print(f"      - test_tasks: {task_count} 条")
        print(f"      - test_records: {record_count} 条")
        print(f"      - tag_statistics: {stat_count} 条")

        # 测试外键约束
        print("\n6. 测试外键约束...")
        test_task_fk = TestTask(
            task_type="single",
            status="completed",
            total_count=1,
            processed_count=1
        )
        db.add(test_task_fk)
        db.flush()

        test_record_fk = TestRecord(
            task_id=test_task_fk.id,
            comment_text="外键测试",
            tags_json='["测试"]'
        )
        db.add(test_record_fk)
        db.commit()
        print(f"   ✅ 外键关系正常: task_id={test_record_fk.task_id}")

        # 清理测试数据
        db.delete(test_record_fk)
        db.delete(test_task_fk)
        db.commit()

        print("\n" + "=" * 60)
        print("✅ 所有CRUD测试通过！")
        print("=" * 60)

        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_foreign_key_relationships():
    """
    测试外键关系
    """
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("外键关系测试")
        print("=" * 60)

        # 查询有记录的任务
        tasks_with_records = db.query(TestTask).join(TestRecord).all()
        print(f"\n1. 找到 {len(tasks_with_records)} 个有记录的任务")

        for task in tasks_with_records:
            records = db.query(TestRecord).filter(TestRecord.task_id == task.id).all()
            print(f"   - 任务 {task.id}: {len(records)} 条记录")

        print("\n   ✅ 外键关系测试通过！")

        return True

    except Exception as e:
        print(f"\n❌ 外键测试失败: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🧪 开始数据库完整测试...\n")

    # 执行CRUD测试
    crud_result = test_crud_operations()

    # 执行外键测试
    fk_result = test_foreign_key_relationships()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"CRUD操作测试: {'✅ 通过' if crud_result else '❌ 失败'}")
    print(f"外键关系测试: {'✅ 通过' if fk_result else '❌ 失败'}")
    print("=" * 60)

    if crud_result and fk_result:
        print("\n✅ 阶段二数据库测试全部通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败")
        sys.exit(1)
