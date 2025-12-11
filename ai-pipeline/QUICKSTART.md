# 🚀 快速开始指南

## 5 分钟上手 AI 代码流水线

### 📋 前置要求

- Python 3.11+
- OpenAI API Key 或 Claude API Key
- Git (可选,用于自动提交)

---

## 🎯 方式一: 使用安装脚本 (推荐)

### Windows

```cmd
# 1. 克隆仓库
git clone <your-repo-url>
cd ai-pipeline

# 2. 运行安装脚本
setup.bat

# 3. 编辑 .env 文件
notepad .env
# 设置: OPENAI_API_KEY=your-key-here

# 4. 运行流水线
python orchestrator\orchestrator.py --requirement "创建一个待办事项 API"
```

### Linux / macOS

```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd ai-pipeline

# 2. 运行安装脚本
chmod +x setup.sh
./setup.sh

# 3. 编辑 .env 文件
nano .env
# 设置: OPENAI_API_KEY=your-key-here

# 4. 运行流水线
python orchestrator/orchestrator.py --requirement "创建一个待办事项 API"
```

---

## 🔧 方式二: 手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env,设置 API Key

# 5. 运行流水线
python orchestrator/orchestrator.py --requirement "你的需求"
```

---

## 🎬 无需 API Key 的演示

如果你只想快速了解流水线的工作原理,可以运行演示脚本:

```bash
# 完整流程演示 (使用模拟数据)
python demo.py --full

# 工具函数演示
python demo.py --utils
```

---

## 📝 使用示例

### 示例 1: 创建 REST API

```bash
python orchestrator/orchestrator.py \
  --requirement "创建一个用户认证 REST API,支持注册、登录、登出,使用 JWT token"
```

**预期输出:**
- 完整的 Flask/FastAPI 应用
- 用户模型和数据库配置
- JWT 认证中间件
- 单元测试

### 示例 2: 数据处理工具

```bash
python orchestrator/orchestrator.py \
  --requirement "创建一个 CSV 数据清洗工具,支持去重、填充缺失值、数据验证"
```

**预期输出:**
- Python 脚本或模块
- 数据验证规则
- 命令行接口
- 示例用法和测试

### 示例 3: 微服务

```bash
python orchestrator/orchestrator.py \
  --requirement "创建一个订单管理微服务,使用 GraphQL API,支持创建、查询、更新订单"
```

**预期输出:**
- GraphQL schema 定义
- Resolver 实现
- 数据库模型
- API 文档

---

## 📂 查看输出

生成的代码保存在临时目录:

```bash
# Linux/macOS
ls -la /tmp/ai_pipeline_output/

# Windows
dir %TEMP%\ai_pipeline_output\
```

**目录结构:**

```
ai_pipeline_output/
├── step1_srs.json           # 需求分析结果
├── step2_code.json          # 代码生成记录
├── step3_review.json        # 审查结果
├── step4_fix.json           # 修复记录 (如有)
└── generated_code/          # 最终代码
    ├── src/
    ├── tests/
    └── requirements.txt
```

---

## 🧪 测试示例应用

仓库包含一个完整的示例应用,可以直接运行:

```bash
# 运行 Flask 应用
python example_app/src/app.py

# 在另一个终端测试 API
curl http://localhost:5000/health
curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"a":10,"b":5}'

# 运行测试
pytest example_app/tests/ -v
```

---

## 🐳 使用 Docker

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
  python orchestrator/orchestrator.py --requirement "创建一个博客 API"
```

### 运行示例应用

```bash
docker run -p 5000:5000 ai-pipeline python example_app/src/app.py
```

---

## ⚙️ 配置选项

### 环境变量

在 `.env` 文件中配置:

```bash
# LLM 提供商 (openai 或 anthropic)
LLM_PROVIDER=openai

# API Keys
OPENAI_API_KEY=sk-your-openai-key
CLAUDE_API_KEY=sk-ant-your-claude-key  # 可选

# 自动提交到 Git (true 或 false)
AUTO_GIT_COMMIT=false
```

### 命令行参数

```bash
# 基本用法
python orchestrator/orchestrator.py --requirement "需求描述"

# 设置最大修复迭代次数
python orchestrator/orchestrator.py \
  --requirement "需求描述" \
  --max-iterations 3
```

---

## 🔍 故障排查

### 问题 1: API 调用失败

**错误信息:**
```
RuntimeError: OpenAI API 调用失败: 401 Unauthorized
```

**解决方案:**
```bash
# 检查 API Key
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY%  # Windows

# 重新设置
export OPENAI_API_KEY="sk-your-correct-key"
```

### 问题 2: 依赖安装失败

**错误信息:**
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案:**
```bash
# 升级 pip
pip install --upgrade pip

# 清除缓存重装
pip cache purge
pip install -r requirements.txt
```

### 问题 3: 代码未生成

**可能原因:**
- 提示词不够明确
- LLM 响应格式不符合预期

**解决方案:**
```bash
# 查看中间结果
cat /tmp/ai_pipeline_output/step2_code.json

# 使用更具体的需求描述
python orchestrator/orchestrator.py \
  --requirement "创建一个 Flask REST API,包含用户 CRUD 操作,使用 SQLite 数据库,包含单元测试"
```

### 问题 4: 测试失败

**检查清单:**
- [ ] 虚拟环境已激活
- [ ] 依赖已安装完整
- [ ] Python 版本正确 (3.11+)

```bash
# 重新安装依赖
pip install -r requirements.txt

# 运行特定测试
pytest example_app/tests/test_app.py::test_health -v
```

---

## 📚 下一步

- 📖 阅读 [README.md](README.md) 了解详细功能
- 🏗️ 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解架构
- 🤝 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 参与贡献
- 🐛 遇到问题? 提交 [Issue](https://github.com/your-repo/issues)

---

## 💡 使用技巧

### 技巧 1: 精确的需求描述

**好的需求:**
```
创建一个用户认证 REST API,使用 Flask 框架,支持:
1. 用户注册 (邮箱+密码)
2. 登录返回 JWT token
3. Token 验证中间件
4. 使用 SQLite 数据库
5. 包含完整的单元测试
```

**不好的需求:**
```
做一个登录功能
```

### 技巧 2: 迭代改进

如果第一次生成的代码不满意:

```bash
# 第一次运行
python orchestrator/orchestrator.py --requirement "创建一个计算器 API"

# 查看输出后,使用更详细的需求
python orchestrator/orchestrator.py --requirement "创建一个科学计算器 REST API,支持基本运算、三角函数、对数函数,返回 JSON 格式,包含输入验证和错误处理"
```

### 技巧 3: 结合示例代码

```bash
# 参考示例应用的风格
python orchestrator/orchestrator.py --requirement "参考 example_app 的代码风格,创建一个天气查询 API"
```

---

## 🎓 学习资源

- [Flask 文档](https://flask.palletsprojects.com/)
- [pytest 文档](https://docs.pytest.org/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic Claude 文档](https://docs.anthropic.com/)

---

**准备好了吗? 开始你的第一个 AI 代码生成之旅!** 🚀

```bash
python orchestrator/orchestrator.py --requirement "创建一个简单的博客 API"
```
