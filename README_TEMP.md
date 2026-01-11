# 用户画像Agent测试系统

一个用于测试Dify工作流"获取用户评论标签"的前后端测试系统，为用户画像agent系统提供验证工具。

## 🎯 项目简介

本系统用于测试汽车用户评论的标签提取功能，通过调用Dify Cloud API对评论进行情感分析、标签提取和分类统计，为全量评论标签训练提供验证工具。

## ✨ 核心功能

- ✅ **单条评论测试**: 输入单条评论，实时获取标签分析结果
- ✅ **批量CSV测试**: 上传CSV文件，批量处理评论（最多1000条）
- ✅ **实时进度跟踪**: 后台任务处理，前端轮询显示进度
- ✅ **统计分析**: 标签分布柱状图、分类饼图、数据洞察
- ✅ **历史记录**: 任务列表、详情查看、数据导出（CSV/Excel/JSON）

## 🛠️ 技术栈

### 后端
- **Python**: 3.9.6
- **Web框架**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23
- **数据库**: SQLite
- **HTTP客户端**: httpx 0.25.1
- **数据处理**: pandas 2.1.3

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite 5.4.21
- **UI组件**: Ant Design 5.12.0
- **路由**: React Router DOM 6.20.0
- **图表**: ECharts 5.6.0 + echarts-for-react 3.0.5
- **HTTP客户端**: Axios 1.6.2

### 外部服务
- **Dify Cloud API**: https://api.dify.ai/v1
- **工作流**: get_comment_tags
- **API Key**: app-33QFU9RLluraZy9P92lDGjHc

## 📁 项目结构

```
user-profile-agent-test/
├── backend/                 # 后端FastAPI项目
│   ├── app/
│   │   ├── main.py         # FastAPI入口
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   ├── models/         # SQLAlchemy模型
│   │   │   ├── task.py     # 测试任务模型
│   │   │   ├── record.py   # 测试记录模型
│   │   │   └── statistic.py# 标签统计模型
│   │   ├── schemas/        # Pydantic schemas
│   │   │   ├── test.py     # 测试相关schemas
│   │   │   ├── batch.py    # 批量测试schemas
│   │   │   └── statistics.py # 统计schemas
│   │   ├── api/            # API路由
│   │   │   ├── test.py     # 测试API
│   │   │   └── statistics.py # 统计API
│   │   ├── services/       # 业务逻辑
│   │   │   ├── dify_client.py    # Dify客户端
│   │   │   ├── test_service.py   # 测试服务
│   │   │   ├── batch_test_service.py # 批量测试服务
│   │   │   └── stats_service.py   # 统计服务
│   │   └── utils/         # 工具函数
│   │       └── csv_parser.py # CSV解析工具
│   ├── requirements.txt
│   └── run.py
├── frontend/               # 前端React项目
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/           # API调用封装
│   │   │   ├── client.ts
│   │   │   ├── test.ts
│   │   │   └── statistics.ts
│   │   ├── pages/         # 页面组件
│   │   │   ├── SingleTestPage.tsx
│   │   │   ├── BatchTestPage.tsx
│   │   │   └── StatisticsPage.tsx
│   │   ├── components/    # 公共组件
│   │   │   ├── CommentInput.tsx
│   │   │   ├── TagDisplay.tsx
│   │   │   ├── FileUploader.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   ├── TagChart.tsx
│   │   │   └── CategoryChart.tsx
│   │   └── types/         # TypeScript类型定义
│   │       ├── test.ts
│   │       ├── batch.ts
│   │       └── statistics.ts
│   ├── package.json
│   └── vite.config.ts
├── data/                  # 数据存储目录
│   └── uploads/          # 上传文件存储
├── docs/                 # 文档目录
├── test_reports/         # 测试报告
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python run.py
```

后端服务将在 http://localhost:8000 启动

API文档: http://localhost:8000/docs

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端应用将在 http://localhost:5173 启动

### 配置

**后端配置** (`backend/.env`):
```env
DATABASE_URL=sqlite:///./user_profile_agent.db
DIFY_API_KEY=app-33QFU9RLluraZy9P92lDGjHc
DIFY_BASE_URL=https://api.dify.ai/v1
CORS_ORIGINS=["http://localhost:5173"]
MAX_UPLOAD_SIZE=10485760
```

**前端配置** (`frontend/.env`):
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 📊 功能展示

### 单条测试页面
- 输入评论内容（最多5000字）
- 实时调用Dify API获取标签
- 颜色编码展示标签（正面/负面/中立）

### 批量测试页面
- 上传CSV文件（最多10MB，1000条评论）
- 支持多种列名：评论、comment、content、text、pinglun
- 实时显示处理进度（已处理/总数/百分比）
- 后台任务异步处理

### 统计分析页面
- 统计概览卡片（总评论数、总标签数、唯一标签、平均处理时间）
- 标签分布柱状图（Top 10）
- 标签分类饼图（8大分类：正面情感、负面情感、产品性能、外观设计等）
- 数据洞察说明

## 🎨 API端点

### 测试相关

- `POST /api/v1/test/single` - 单条评论测试
- `POST /api/v1/test/batch/upload` - 批量测试上传
- `GET /api/v1/test/batch/progress/{task_id}` - 查询批量任务进度
- `GET /api/v1/test/task/{task_id}` - 获取任务详情

### 统计相关

- `GET /api/v1/statistics/overview?task_id={id}` - 获取统计概览

## 🧪 测试

### 后端测试

```bash
cd backend
pytest
```

### 前端测试

```bash
cd frontend
npm test
```

## 📝 CSV文件格式

批量测试支持CSV文件格式：

```csv
评论
这款车的动力太棒了！
油耗有点高，不推荐
外观设计很时尚
```

支持的列名：评论、comment、content、text、pinglun、评论内容、用户评论

## 🔧 开发说明

### 数据库设计

**test_tasks (测试任务表)**
- id: 主键
- task_type: 'single' 或 'batch'
- status: 'pending', 'processing', 'completed', 'failed'
- total_count: 总评论数
- processed_count: 已处理数
- created_at, updated_at, completed_at
- error_message: 错误信息

**test_records (测试记录表)**
- id: 主键
- task_id: 关联test_tasks
- comment_text: 评论内容
- tags_json: JSON格式标签
- confidence: 置信度
- processing_time: 处理耗时
- created_at

### Dify API集成

- Base URL: https://api.dify.ai/v1
- 端点: /workflows/run
- 参数: inputs.pinglun (评论内容)
- 响应: outputs.text (JSON格式标签)

## 📈 测试报告

所有测试报告位于 `test_reports/` 目录：

- stage1_test_report.md - 项目初始化
- stage2_test_report.md - 数据库搭建
- stage3_test_report.md - Dify API集成
- stage4_5_test_report.md - 单条测试功能
- stage6_stage7_test_report.md - 批量测试功能
- stage8_test_report.md - 统计分析API
- stage9_test_report.md - 统计分析页面

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👤 作者

dedede (199714353)

## 🙏 致谢

- [Dify](https://dify.ai/) - AI工作流平台
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [React](https://react.dev/) - 用户界面JavaScript库
- [Ant Design](https://ant.design/) - 企业级UI设计语言
- [ECharts](https://echarts.apache.org/) - 强大的图表库
