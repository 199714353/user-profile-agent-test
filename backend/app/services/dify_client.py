"""
Dify API客户端
用于调用Dify工作流API
"""
import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from app.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DifyClientError(Exception):
    """Dify客户端异常"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DifyClient:
    """
    Dify API客户端类
    用于调用Dify Cloud API的工作流
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化Dify客户端

        Args:
            api_key: Dify API密钥，默认从配置读取
            base_url: Dify API基础URL，默认从配置读取
        """
        self.api_key = api_key or settings.DIFY_API_KEY
        self.base_url = base_url or settings.DIFY_BASE_URL
        self.timeout = 30.0  # 默认超时30秒
        self.max_retries = 3  # 最大重试次数

        logger.info(f"Dify客户端初始化: base_url={self.base_url}")

    async def get_comment_tags(
        self,
        comment: str,
        user: str = "test_system_user"
    ) -> Dict[str, Any]:
        """
        调用Dify工作流获取评论标签

        Args:
            comment: 用户评论文本
            user: 用户标识，默认为"test_system_user"

        Returns:
            包含标签和置信度的字典:
            {
                "tags": List[str],           # 提取的标签列表
                "confidence": float,          # 置信度（如果Dify返回）
                "raw_response": Dict,        # Dify原始响应
                "processing_time": float     # 处理时间（毫秒）
            }

        Raises:
            DifyClientError: API调用失败时抛出
        """
        import time

        url = f"{self.base_url}/workflows/run"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": {
                "pinglun": comment  # Dify工作流使用"pinglun"作为输入参数名
            },
            "response_mode": "blocking",
            "user": user
        }

        # 记录开始时间
        start_time = time.time()

        # 带重试的API调用
        for attempt in range(self.max_retries):
            try:
                logger.info(f"调用Dify API (尝试 {attempt + 1}/{self.max_retries})")
                logger.debug(f"URL: {url}")
                logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")

                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        url,
                        json=payload,
                        headers=headers
                    )

                    # 计算处理时间
                    processing_time = (time.time() - start_time) * 1000

                    # 检查HTTP状态码
                    if response.status_code != 200:
                        error_msg = f"Dify API返回错误状态码: {response.status_code}"
                        logger.error(f"{error_msg}, 响应: {response.text}")
                        raise DifyClientError(
                            error_msg,
                            status_code=response.status_code
                        )

                    # 解析响应
                    result = response.json()
                    logger.info(f"Dify API调用成功，耗时: {processing_time:.2f}ms")
                    logger.debug(f"响应: {json.dumps(result, ensure_ascii=False)}")

                    # 解析并返回结果
                    return self._parse_dify_response(result, processing_time)

            except httpx.TimeoutException as e:
                logger.warning(f"请求超时 (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    raise DifyClientError(f"Dify API请求超时: {str(e)}")

            except httpx.HTTPError as e:
                logger.warning(f"HTTP错误 (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    raise DifyClientError(f"Dify API调用失败: {str(e)}")

            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {str(e)}")
                logger.error(f"响应内容: {response.text}")
                raise DifyClientError(f"Dify API响应格式错误: {str(e)}")

    def _parse_dify_response(
        self,
        response: Dict,
        processing_time: float
    ) -> Dict[str, Any]:
        """
        解析Dify返回结果

        Args:
            response: Dify API原始响应
            processing_time: 处理时间（毫秒）

        Returns:
            解析后的结果字典
        """
        try:
            # Dify工作流响应格式
            # {
            #     "task_id": "...",
            #     "workflow_run_id": "...",
            #     "data": {
            #         "id": "workflow_id",
            #         "status": "succeeded",
            #         "outputs": {
            #             "text": "{\\"维度\\": \\"动力\\", \\"值\\": \\"正面\\"}"
            #         },
            #         ...
            #     }
            # }

            # 获取data部分
            data = response.get("data", {})

            # 检查workflow执行状态
            status = data.get("status", "")
            if status != "succeeded":
                error_msg = data.get("error", "工作流执行失败")
                logger.error(f"Dify工作流执行失败: {status}, error: {error_msg}")
                logger.debug(f"完整响应: {json.dumps(response, ensure_ascii=False)}")
                raise DifyClientError(f"Dify工作流执行失败: {error_msg}")

            outputs = data.get("outputs", {})

            # 提取标签
            tags = []

            # 优先从text字段读取（Dify工作流返回格式）
            if "text" in outputs:
                text_output = outputs["text"]
                try:
                    # 解析JSON字符串
                    parsed = json.loads(text_output)

                    # 提取维度和值
                    if "维度" in parsed and "值" in parsed:
                        dimension = parsed["维度"]
                        value = parsed["值"]
                        tags = [f"{dimension}:{value}"]
                        # 也可以作为两个独立标签
                        tags.extend([dimension, value])
                    else:
                        # 如果是其他格式，作为单个标签
                        tags = [text_output]

                except json.JSONDecodeError:
                    # 如果不是JSON，作为单个标签
                    tags = [text_output]

            # 兼容：如果没有text字段，尝试tags字段
            elif "tags" in outputs:
                tags_value = outputs["tags"]
                if isinstance(tags_value, list):
                    tags = tags_value
                elif isinstance(tags_value, str):
                    try:
                        tags = json.loads(tags_value)
                    except json.JSONDecodeError:
                        tags = [tags_value]
            else:
                # 如果没有找到标签字段，记录所有输出
                logger.warning(f"响应中未找到预期的标签字段，输出: {outputs}")
                # 尝试从其他字段提取
                for key, value in outputs.items():
                    if value:
                        tags.append(str(value))

            # 提取置信度
            confidence = 0.0
            if "confidence" in outputs:
                try:
                    confidence = float(outputs["confidence"])
                except (ValueError, TypeError):
                    pass

            return {
                "tags": tags,
                "confidence": confidence,
                "raw_response": response,
                "processing_time": processing_time
            }

        except Exception as e:
            logger.error(f"解析Dify响应失败: {str(e)}")
            logger.debug(f"响应内容: {json.dumps(response, ensure_ascii=False)}")
            raise DifyClientError(f"解析Dify响应失败: {str(e)}")

    async def health_check(self) -> bool:
        """
        检查Dify API连接状态

        Returns:
            bool: 连接正常返回True，否则返回False
        """
        try:
            # 使用一个简单的测试评论
            test_comment = "测试连接"
            result = await self.get_comment_tags(test_comment)
            logger.info("Dify API健康检查通过")
            return True
        except Exception as e:
            logger.error(f"Dify API健康检查失败: {str(e)}")
            return False


# 创建全局实例
dify_client = DifyClient()
