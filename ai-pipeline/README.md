# 🤖 AI 自动化代码流水线

[![CI Status](https://img.shields.io/badge/CI-passing-brightgreen)](https://github.com)
[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**端到端的 AI 驱动代码生成流水线**,从自然语言需求到可运行代码,完全自动化。

## 🎯 核心特性

- ✅ **需求到代码全自动**: 输入需求描述,输出可运行的完整代码
- 🔄 **多 LLM 协作**: Codex 负责 SRS 和审查,Claude 负责代码生成
- 🧪 **自动测试**: 生成单元测试并自动执行
- 🔧 **智能修复**: 自动检测缺陷并迭代修复
- 🐳 **容器化支持**: Docker 镜像开箱即用
- 🚀 **CI/CD 集成**: GitHub Actions 自动化工作流

## 📋 流程概览

```
用户需求 ──┬──> [Codex] 生成 SRS
           │            │
           │            v
           └──> [Claude] 生成代码
                        │
                        v
           ┌──> [Codex] 审查 & 测试
           │            │
           │            v
           │    ┌──── 通过? ────┐
           │    │ Yes          │ No
           │    v              v
           │ 提交代码    [Claude] 修复
           └──────────────────┘
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone <your-repo-url>
cd ai-pipeline

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
export OPENAI_API_KEY="your-openai-key"
export CLAUDE_API_KEY="your-claude-key"  # 可选,如果使用 Anthropic
export LLM_PROVIDER="openai"  # 或 "anthropic"
```

### 2. 运行流水线

```bash
python orchestrator/orchestrator.py --requirement "创建一个用户认证 REST API,支持注册、登录和 JWT"
```

### 3. 查看结果

生成的代码和中间结果保存在 `/tmp/ai_pipeline_output/`:

```
/tmp/ai_pipeline_output/
├── step1_srs.json           # SRS 文档
├── step2_code.json          # 生成的代码
├── step3_review.json        # 审查结果
├── step4_fix.json           # 修复记录 (如有)
└── generated_code/          # 最终代码
    ├── src/
    ├── tests/
    └── requirements.txt
```

## 📚 详细文档

### 配置选项

#### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | - | ✅ (如使用 OpenAI) |
| `CLAUDE_API_KEY` | Claude API 密钥 | - | ✅ (如使用 Anthropic) |
| `LLM_PROVIDER` | LLM 提供商 | `openai` | ❌ |
| `AUTO_GIT_COMMIT` | 自动提交到 Git | `false` | ❌ |

#### 命令行参数

```bash
python orchestrator/orchestrator.py \
  --requirement "需求描述" \
  --max-iterations 3  # 最大修复迭代次数,默认 2
```

### 示例微服务

仓库包含一个完整的 Flask 微服务示例 ([example_app/](example_app/)):

```bash
# 运行示例应用
python example_app/src/app.py

# 运行测试
pytest example_app/tests/ -v
```

**API 端点:**

- `GET /health` - 健康检查
- `POST /add` - 加法运算
- `POST /multiply` - 乘法运算
- `POST /divide` - 除法运算

**示例请求:**

```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'

# 响应: {"result": 15, "operation": "add"}
```

## 🐳 Docker 使用

### 构建镜像

```bash
docker build -t ai-pipeline:latest .
```

### 运行流水线

```bash
docker run --rm \
  -e OPENAI_API_KEY="your-key" \
  -v $(pwd)/output:/app/output \
  ai-pipeline \
  python orchestrator/orchestrator.py --requirement "创建一个 TODO API"
```

### 运行示例应用

```bash
docker run -p 5000:5000 \
  ai-pipeline \
  python example_app/src/app.py
```

## 🔧 高级用法

### 自定义提示词模板

编辑 [orchestrator/prompts/](orchestrator/prompts/) 下的模板文件:

- `codex_srs_prompt.txt` - SRS 生成提示词
- `claude_code_prompt.txt` - 代码生成提示词
- `codex_review_prompt.txt` - 代码审查提示词

### 修改 LLM 模型

编辑 [orchestrator/llm_client.py](orchestrator/llm_client.py:36-45):

```python
# 修改 Codex 模型
response = client.chat.completions.create(
    model='gpt-4-turbo-preview',  # 改为你想用的模型
    ...
)

# 修改 Claude 模型
response = client.messages.create(
    model='claude-3-5-sonnet-20241022',  # 改为你想用的模型
    ...
)
```

### 集成到 CI/CD

#### GitHub Actions

仓库已包含 [.github/workflows/ai-pipeline.yml](.github/workflows/ai-pipeline.yml)。

**手动触发工作流:**

1. 前往 GitHub Actions 页面
2. 选择 "AI Pipeline CI"
3. 点击 "Run workflow"
4. 输入需求描述

**配置 Secrets:**

在 GitHub 仓库设置中添加:

- `OPENAI_API_KEY`
- `CLAUDE_API_KEY` (可选)
- `LLM_PROVIDER` (可选)
- `DOCKER_USERNAME` / `DOCKER_PASSWORD` (可选,用于推送镜像)

#### GitLab CI

创建 `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build

test:
  stage: test
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - pytest example_app/tests/ -v

build-docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t ai-pipeline:$CI_COMMIT_SHA .
```

## 🧪 测试

```bash
# 运行所有测试
pytest example_app/tests/ -v

# 运行特定测试
pytest example_app/tests/test_app.py::TestAddEndpoint -v

# 生成覆盖率报告
pytest example_app/tests/ --cov=example_app --cov-report=html
```

## 🛠️ 故障排除

### 常见问题

**Q: API 调用失败,显示 401 Unauthorized**

A: 检查 API Key 是否正确设置:
```bash
echo $OPENAI_API_KEY
echo $CLAUDE_API_KEY
```

**Q: 生成的代码没有通过审查**

A: 增加 `--max-iterations` 参数:
```bash
python orchestrator/orchestrator.py --requirement "..." --max-iterations 5
```

**Q: 解析不出代码块**

A: 检查提示词模板是否正确,确保要求 LLM 返回带 `# path: ...` 标记的代码块。

**Q: Git 提交失败**

A: 确保:
1. 目标目录是 Git 仓库 (`git init`)
2. 已配置 Git 凭据
3. 设置了 `AUTO_GIT_COMMIT=true`

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH=$(pwd)
python -u orchestrator/orchestrator.py --requirement "..." 2>&1 | tee pipeline.log
```

## 🏗️ 架构设计

### 核心组件

```
orchestrator/
├── orchestrator.py      # 主流程编排器
├── llm_client.py        # LLM API 客户端封装
├── utils.py             # 工具函数 (文件操作、Git 操作)
└── prompts/             # 提示词模板
    ├── codex_srs_prompt.txt
    ├── claude_code_prompt.txt
    └── codex_review_prompt.txt
```

### 设计原则

- **KISS (Keep It Simple)**: 代码逻辑简单直观,避免过度抽象
- **YAGNI (You Aren't Gonna Need It)**: 只实现当前需要的功能
- **DRY (Don't Repeat Yourself)**: 共用逻辑抽取为工具函数
- **错误容错**: API 调用支持重试,解析失败有降级处理
- **可观察性**: 每步输出详细日志,中间结果持久化

## 🤝 贡献指南

欢迎贡献!请遵循以下步骤:

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

**代码规范:**

- 遵循 PEP 8 (Python)
- 添加单元测试
- 更新相关文档

## 📝 更新日志

### v1.0.0 (2024-01-XX)

- ✨ 初始版本发布
- 🎯 支持 OpenAI 和 Anthropic API
- 🧪 包含完整的示例应用和测试
- 🐳 Docker 镜像支持
- 🚀 GitHub Actions CI/CD

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenAI](https://openai.com) - GPT 模型
- [Anthropic](https://anthropic.com) - Claude 模型
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [pytest](https://pytest.org/) - 测试框架

## 📧 联系方式

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

⭐ 如果这个项目对你有帮助,请给一个 Star!
