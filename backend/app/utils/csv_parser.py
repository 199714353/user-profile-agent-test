"""
CSV文件解析工具
"""
import pandas as pd
import io
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class CSVParser:
    """CSV解析器"""

    # 支持的评论列名
    COMMENT_COLUMNS = ['评论', 'comment', 'content', 'text', 'pinglun', '评论内容', '用户评论']

    # 最大文件大小（10MB）
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # 最大评论数量
    MAX_COMMENTS = 1000

    @staticmethod
    def parse_csv_file(
        file_content: bytes,
        filename: str
    ) -> Tuple[List[str], dict]:
        """
        解析CSV文件，提取评论内容

        Args:
            file_content: CSV文件内容（bytes）
            filename: 文件名

        Returns:
            (评论列表, 文件信息字典)

        Raises:
            ValueError: 文件格式或内容不符合要求时抛出
        """
        # 检查文件大小
        file_size = len(file_content)
        if file_size > CSVParser.MAX_FILE_SIZE:
            raise ValueError(f"文件大小超过限制（{CSVParser.MAX_FILE_SIZE / 1024 / 1024}MB）")

        # 检查文件扩展名
        if not filename.lower().endswith('.csv'):
            raise ValueError("只支持CSV文件格式")

        try:
            # 读取CSV文件
            df = pd.read_csv(io.BytesIO(file_content))

            logger.info(f"CSV文件读取成功，列名: {df.columns.tolist()}")

            # 自动识别评论列
            comment_col = CSVParser._identify_comment_column(df)

            if not comment_col:
                raise ValueError(
                    f"CSV文件中未找到评论列。支持的列名: {', '.join(CSVParser.COMMENT_COLUMNS)}"
                )

            # 提取评论
            comments = df[comment_col].dropna().tolist()

            # 过滤空字符串
            comments = [c.strip() for c in comments if c and c.strip()]

            # 检查评论数量
            if len(comments) == 0:
                raise ValueError("CSV文件中没有有效的评论数据")

            if len(comments) > CSVParser.MAX_COMMENTS:
                raise ValueError(f"评论数量超过限制（最多{CSVParser.MAX_COMMENTS}条）")

            file_info = {
                'filename': filename,
                'size': file_size,
                'total_rows': len(df),
                'valid_comments': len(comments),
                'comment_column': comment_col
            }

            logger.info(f"CSV解析成功: {file_info}")

            return comments, file_info

        except pd.errors.EmptyDataError:
            raise ValueError("CSV文件为空")
        except pd.errors.ParserError as e:
            raise ValueError(f"CSV文件格式错误: {str(e)}")
        except Exception as e:
            logger.error(f"CSV解析失败: {str(e)}")
            raise ValueError(f"CSV解析失败: {str(e)}")

    @staticmethod
    def _identify_comment_column(df: pd.DataFrame) -> Optional[str]:
        """
        识别评论列

        Args:
            df: DataFrame对象

        Returns:
            列名，如果未找到返回None
        """
        # 首先尝试精确匹配
        for col in df.columns:
            if col.lower() in [c.lower() for c in CSVParser.COMMENT_COLUMNS]:
                return col

        # 如果没有精确匹配，尝试模糊匹配
        for col in df.columns:
            for valid_col in CSVParser.COMMENT_COLUMNS:
                if valid_col.lower() in col.lower() or col.lower() in valid_col.lower():
                    return col

        # 如果还是没找到，使用第一列
        if len(df.columns) > 0:
            logger.warning(f"未找到标准评论列，使用第一列: {df.columns[0]}")
            return df.columns[0]

        return None
