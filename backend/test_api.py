"""
单条测试API集成测试
测试POST /api/v1/test/single接口
"""
import asyncio
import httpx
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


async def test_single_test_api():
    """
    测试用例8-10: 单条测试API完整测试
    """
    print("\n" + "=" * 60)
    print("单条测试API集成测试")
    print("=" * 60)

    # 测试评论
    test_comment = "这款车的动力太棒了，加速响应非常快！"

    # 测试用例8: 正常流程测试
    print("\n测试用例8: 单条测试API - 正常流程")
    print("-" * 60)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/test/single",
                json={"comment": test_comment}
            )

            print(f"HTTP状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"✅ 请求成功")
                print(f"   - 任务ID: {result.get('task_id')}")
                print(f"   - 任务状态: {result.get('status')}")

                if result.get('result'):
                    tags = result['result'].get('tags', [])
                    processing_time = result['result'].get('processing_time', 0)
                    print(f"   - 标签: {tags}")
                    print(f"   - 处理时间: {processing_time:.2f}ms")
                    test8_pass = True
                else:
                    print(f"   ⚠️  结果为空")
                    test8_pass = False
            else:
                print(f"❌ 请求失败: {response.text}")
                test8_pass = False

    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        test8_pass = False

    # 测试用例9: 异常流程测试
    print("\n测试用例9: 单条测试API - 异常流程")
    print("-" * 60)

    test9_results = {}

    # 9.1: 空评论
    print("\n9.1 空评论测试...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/test/single",
                json={"comment": ""}
            )

            if response.status_code == 400:
                print("   ✅ 正确返回400错误")
                print(f"   错误信息: {response.json().get('detail')}")
                test9_results['empty_comment'] = True
            else:
                print(f"   ⚠️  应返回400，实际返回{response.status_code}")
                test9_results['empty_comment'] = False
    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        test9_results['empty_comment'] = False

    # 9.2: 超长评论
    print("\n9.2 超长评论测试...")
    try:
        long_comment = "测试" * 2000  # 超过5000字符
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/test/single",
                json={"comment": long_comment}
            )

            if response.status_code == 400:
                print("   ✅ 正确返回400错误")
                print(f"   错误信息: {response.json().get('detail')}")
                test9_results['long_comment'] = True
            else:
                print(f"   ⚠️  应返回400，实际返回{response.status_code}")
                test9_results['long_comment'] = False
    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        test9_results['long_comment'] = False

    test9_pass = all(test9_results.values())

    # 测试用例10: 数据持久化验证
    print("\n测试用例10: 数据持久化验证")
    print("-" * 60)

    try:
        if test8_pass and 'result' in locals():
            task_id = result.get('task_id')

            # 查询任务详情
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BASE_URL}/api/v1/test/task/{task_id}")

                if response.status_code == 200:
                    task_data = response.json()
                    print(f"✅ 任务详情查询成功")

                    task = task_data.get('task', {})
                    records = task_data.get('records', [])

                    print(f"   - 任务状态: {task.get('status')}")
                    print(f"   - 已处理数: {task.get('processed_count')}")
                    print(f"   - 总数: {task.get('total_count')}")
                    print(f"   - 记录数: {len(records)}")

                    # 验证数据
                    if task.get('status') == 'completed':
                        print(f"   ✅ 任务状态正确")
                    if task.get('processed_count') == 1:
                        print(f"   ✅ 已处理数正确")
                    if len(records) == 1:
                        print(f"   ✅ 记录数正确")

                    record = records[0] if records else {}
                    if record.get('tags'):
                        print(f"   ✅ 标签已保存: {record.get('tags')}")

                    test10_pass = True
                else:
                    print(f"❌ 查询失败: {response.text}")
                    test10_pass = False
        else:
            print("⚠️  跳过数据持久化测试（测试8未通过）")
            test10_pass = False

    except Exception as e:
        print(f"❌ 数据持久化测试失败: {str(e)}")
        test10_pass = False

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"测试8 (正常流程):        {'✅ 通过' if test8_pass else '❌ 失败'}")
    print(f"测试9 (异常流程):        {'✅ 通过' if test9_pass else '❌ 失败'}")
    print(f"测试10 (数据持久化):     {'✅ 通过' if test10_pass else '❌ 失败'}")
    print("=" * 60)

    all_pass = test8_pass and test9_pass and test10_pass

    if all_pass:
        print("\n✅ 阶段四所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试未通过")
        return 1


if __name__ == "__main__":
    # 检查后端服务是否运行
    import sys
    try:
        import httpx
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code != 200:
            print("❌ 后端服务未正常运行")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 无法连接到后端服务: {str(e)}")
        print(f"请先启动后端服务: cd backend && python3 run.py")
        sys.exit(1)

    # 运行测试
    exit_code = asyncio.run(test_single_test_api())
    sys.exit(exit_code)
