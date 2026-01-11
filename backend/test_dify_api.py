"""
Dify API客户端测试脚本
测试Dify API连接、标签提取和异常处理
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.dify_client import DifyClient, DifyClientError


async def test_dify_connection():
    """
    测试用例5: Dify API连接测试
    """
    print("\n" + "=" * 60)
    print("测试用例5: Dify API连接测试")
    print("=" * 60)

    try:
        client = DifyClient()

        # 检查连接
        print("\n1. 测试API连接...")
        is_connected = await client.health_check()

        if is_connected:
            print("   ✅ Dify API连接成功")
            return True
        else:
            print("   ❌ Dify API连接失败")
            return False

    except Exception as e:
        print(f"   ❌ 连接测试失败: {str(e)}")
        return False


async def test_comment_tagging():
    """
    测试用例6: 单条评论标签提取
    """
    print("\n" + "=" * 60)
    print("测试用例6: 单条评论标签提取")
    print("=" * 60)

    client = DifyClient()

    # 测试评论列表
    test_comments = [
        "这款车的动力太棒了，加速响应非常快！",
        "油耗太高了，市区开要12个油，真心养不起。",
        "车子开了三年，总体还行，没大问题也没小毛病。"
    ]

    results = []

    for idx, comment in enumerate(test_comments, 1):
        try:
            print(f"\n{idx}. 测试评论: {comment[:30]}...")

            result = await client.get_comment_tags(comment)

            print(f"   ✅ 提取成功")
            print(f"   - 标签: {result['tags']}")
            print(f"   - 置信度: {result['confidence']}")
            print(f"   - 处理时间: {result['processing_time']:.2f}ms")

            # 验证结果
            if result['tags'] and len(result['tags']) > 0:
                print(f"   ✅ 标签提取成功，共 {len(result['tags'])} 个标签")
            else:
                print(f"   ⚠️  未提取到标签")

            if result['processing_time'] < 5000:
                print(f"   ✅ 响应时间正常 (< 5秒)")
            else:
                print(f"   ⚠️  响应时间较长: {result['processing_time']:.2f}ms")

            results.append({
                "comment": comment,
                "success": True,
                "tags": result['tags'],
                "processing_time": result['processing_time']
            })

        except Exception as e:
            print(f"   ❌ 提取失败: {str(e)}")
            results.append({
                "comment": comment,
                "success": False,
                "error": str(e)
            })

    # 统计结果
    print("\n" + "-" * 60)
    print("测试统计:")
    total = len(results)
    success = sum(1 for r in results if r['success'])
    avg_time = sum(r.get('processing_time', 0) for r in results if r['success']) / max(success, 1)

    print(f"   - 总测试数: {total}")
    print(f"   - 成功数: {success}")
    print(f"   - 失败数: {total - success}")
    print(f"   - 成功率: {(success/total*100):.1f}%")
    print(f"   - 平均响应时间: {avg_time:.2f}ms")

    if success >= 3:
        print("\n   ✅ 至少3条不同类型的评论成功获取标签")
        return True
    else:
        print(f"\n   ❌ 只有{success}条评论成功，需要至少3条")
        return False


async def test_error_handling():
    """
    测试用例7: 异常处理测试
    """
    print("\n" + "=" * 60)
    print("测试用例7: 异常处理测试")
    print("=" * 60)

    # 测试1: 错误的API Key
    print("\n1. 测试错误API Key...")
    try:
        client = DifyClient(api_key="invalid_api_key_test")
        await client.get_comment_tags("测试评论")
        print("   ⚠️  应该抛出异常但没有")
        test1_pass = False
    except DifyClientError as e:
        print(f"   ✅ 正确捕获异常: {e.message}")
        test1_pass = True
    except Exception as e:
        print(f"   ⚠️  捕获到其他异常: {str(e)}")
        test1_pass = False

    # 测试2: 空评论（某些API可能接受）
    print("\n2. 测试空评论...")
    try:
        client = DifyClient()
        result = await client.get_comment_tags("")
        print(f"   ✅ API接受空评论，返回标签: {result['tags']}")
        test2_pass = True
    except DifyClientError as e:
        print(f"   ✅ API拒绝空评论，正确返回错误: {e.message}")
        test2_pass = True
    except Exception as e:
        print(f"   ⚠️  未知错误: {str(e)}")
        test2_pass = False

    # 测试3: 超长评论
    print("\n3. 测试超长评论...")
    try:
        client = DifyClient()
        long_comment = "测试评论" * 1000  # 约5000字
        result = await client.get_comment_tags(long_comment)
        print(f"   ✅ API接受超长评论，返回标签: {result['tags']}")
        test3_pass = True
    except DifyClientError as e:
        print(f"   ✅ API拒绝超长评论，正确返回错误: {e.message}")
        test3_pass = True
    except Exception as e:
        print(f"   ⚠️  未知错误: {str(e)}")
        test3_pass = False

    all_pass = test1_pass and test2_pass and test3_pass

    print("\n" + "-" * 60)
    print(f"异常处理测试: {'✅ 通过' if all_pass else '❌ 部分失败'}")

    return all_pass


async def run_all_tests():
    """
    运行所有测试
    """
    from app.config import settings

    print("\n" + "=" * 60)
    print("🧪 Dify API客户端测试")
    print("=" * 60)

    print("\n配置信息:")
    print(f"   - API Key: {settings.DIFY_API_KEY[:20]}...")
    print(f"   - Base URL: {settings.DIFY_BASE_URL}")

    # 执行测试
    test_results = {}

    # 测试5: 连接测试
    test_results['test5'] = await test_dify_connection()

    # 测试6: 标签提取测试
    test_results['test6'] = await test_comment_tagging()

    # 测试7: 异常处理测试
    test_results['test7'] = await test_error_handling()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"测试5 (连接测试):        {'✅ 通过' if test_results['test5'] else '❌ 失败'}")
    print(f"测试6 (标签提取):        {'✅ 通过' if test_results['test6'] else '❌ 失败'}")
    print(f"测试7 (异常处理):        {'✅ 通过' if test_results['test7'] else '❌ 失败'}")
    print("=" * 60)

    all_pass = all(test_results.values())

    if all_pass:
        print("\n✅ 阶段三所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试未通过，请检查配置和网络连接")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
