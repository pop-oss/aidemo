# 项目结构说明

```
ai-pipeline/
│
├── 📋 配置文件
│   ├── requirements.txt          # Python 依赖
│   ├── Dockerfile                # Docker 镜像配置
│   ├── .env.example              # 环境变量示例
│   ├── .gitignore                # Git 忽略规则
│   ├── LICENSE                   # MIT 许可证
│   ├── setup.sh                  # Linux/Mac 快速设置脚本
│   └── setup.bat                 # Windows 快速设置脚本
│
├── 📚 文档
│   ├── README.md                 # 项目主文档
│   ├── CONTRIBUTING.md           # 贡献指南
│   └── PROJECT_STRUCTURE.md      # 本文件
│
├── 🤖 核心编排器 (orchestrator/)
│   ├── orchestrator.py           # 主流程编排器
│   ├── llm_client.py             # LLM API 客户端封装
│   ├── utils.py                  # 工具函数 (文件、Git 操作)
│   └── prompts/                  # 提示词模板目录
│       ├── codex_srs_prompt.txt     # SRS 生成提示词
│       ├── claude_code_prompt.txt   # 代码生成提示词
│       └── codex_review_prompt.txt  # 代码审查提示词
│
├── 🧪 示例应用 (example_app/)
│   ├── __init__.py
│   ├── pyproject.toml            # 项目配置
│   ├── src/                      # 源代码
│   │   ├── __init__.py
│   │   └── app.py                # Flask 微服务
│   └── tests/                    # 测试代码
│       ├── __init__.py
│       └── test_app.py           # 单元测试
│
├── 🚀 CI/CD (.github/)
│   └── workflows/
│       └── ai-pipeline.yml       # GitHub Actions 工作流
│
└── 🎬 演示脚本
    └── demo.py                   # 流水线演示 (无需 API Key)
```

## 核心模块说明

### 1. orchestrator.py - 主编排器

**职责:**
- 协调整个 AI 代码生成流水线
- 调用各个 LLM 完成不同任务
- 处理错误和重试逻辑
- 管理中间结果持久化

**主要函数:**
- `main()` - 主流程入口
- `generate_srs()` - 生成 SRS
- `generate_code()` - 生成代码
- `review_and_test()` - 审查和测试
- `fix_defects()` - 修复缺陷

**执行流程:**
```
用户需求
  ↓
生成 SRS (Codex)
  ↓
生成代码 (Claude)
  ↓
写入文件系统
  ↓
审查测试 (Codex)
  ↓
通过? ──Yes→ [可选] 提交 Git
  ↓ No
修复缺陷 (Claude)
  ↓
重新审查 (最多 N 次)
```

### 2. llm_client.py - LLM 客户端

**职责:**
- 统一封装多个 LLM 提供商的 API
- 处理 API 调用细节
- 实现重试机制

**支持的提供商:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3.5)

**主要方法:**
- `call_codex()` - 调用 Codex (用于分析和审查)
- `call_claude()` - 调用 Claude (用于代码生成)
- `call_with_retry()` - 带重试的 API 调用

### 3. utils.py - 工具函数

**职责:**
- 文件系统操作
- Git 操作
- JSON 解析和验证
- 中间结果保存

**主要函数:**
- `write_files_from_codeblock()` - 将代码块写入文件
- `commit_and_push()` - Git 提交和推送
- `validate_json_response()` - 智能 JSON 解析
- `save_intermediate_result()` - 保存中间结果

### 4. 提示词模板 (prompts/)

**codex_srs_prompt.txt:**
- 将自然语言需求转换为结构化 SRS
- 输出: JSON 格式 (srs + tasks)

**claude_code_prompt.txt:**
- 根据 SRS 生成完整可运行代码
- 输出: 带路径标记的代码块

**codex_review_prompt.txt:**
- 审查代码质量、安全性、性能
- 生成单元测试
- 输出: JSON 格式 (passed + defects + tests)

## 示例应用说明

### example_app/src/app.py

**Flask 微服务示例:**
- 健康检查端点: `GET /health`
- 计算端点: `POST /add`, `/multiply`, `/divide`
- 完整的错误处理和日志记录
- 遵循 RESTful 最佳实践

### example_app/tests/test_app.py

**完整的测试套件:**
- 功能测试: 验证正常输入
- 边界测试: 除零、空输入等
- 错误处理测试: 无效输入、方法不允许
- 使用 pytest 框架

## 数据流说明

### 输入

```bash
python orchestrator/orchestrator.py --requirement "创建用户认证 API"
```

### 中间输出 (保存到 /tmp/ai_pipeline_output/)

```
step1_srs.json:
{
  "srs": "# 用户认证 API\n...",
  "tasks": [...]
}

step2_code.json:
{
  "code_blocks": [
    {"path": "auth/api.py", "content": "..."},
    ...
  ]
}

step3_review.json:
{
  "passed": true,
  "defects": [],
  "tests": {...}
}
```

### 最终输出

```
generated_code/
├── auth/
│   ├── api.py
│   ├── models.py
│   └── utils.py
├── tests/
│   └── test_auth.py
└── requirements.txt
```

## 配置说明

### 必需的环境变量

```bash
# 选择其一
export OPENAI_API_KEY="sk-..."
export CLAUDE_API_KEY="sk-ant-..."

# 指定提供商
export LLM_PROVIDER="openai"  # 或 "anthropic"
```

### 可选的环境变量

```bash
# 自动提交到 Git
export AUTO_GIT_COMMIT="true"

# 自定义输出目录
export OUTPUT_DIR="/path/to/output"

# 日志级别
export LOG_LEVEL="DEBUG"
```

## 扩展点

### 1. 添加新的 LLM 提供商

在 `llm_client.py` 中:

```python
def call_new_provider(self, prompt, max_tokens):
    # 实现新提供商的 API 调用
    pass
```

### 2. 自定义提示词模板

编辑 `orchestrator/prompts/*.txt` 文件,调整提示词以适应特定需求。

### 3. 添加额外的审查步骤

在 `orchestrator.py` 中添加新的审查函数:

```python
def security_review(client, code):
    # 专门的安全审查
    pass
```

### 4. 集成其他工具

- 静态代码分析 (pylint, mypy)
- 代码格式化 (black, prettier)
- 依赖检查 (safety, snyk)

## 性能考虑

### API 调用开销

- SRS 生成: ~5-10 秒
- 代码生成: ~15-30 秒
- 代码审查: ~10-15 秒
- 缺陷修复: ~10-20 秒

**总时间:** 约 1-2 分钟 (取决于项目复杂度)

### 优化建议

1. **并行化:** 某些步骤可以并行执行
2. **缓存:** 缓存相似需求的 SRS
3. **流式输出:** 使用 streaming API 加快响应
4. **本地模型:** 考虑使用本地部署的模型

## 安全注意事项

### ⚠️ 重要安全提示

1. **API Key 保护:**
   - 永远不要提交 `.env` 文件
   - 使用 Secret Manager (生产环境)
   - 定期轮换 API Key

2. **代码审查:**
   - 始终人工审查生成的代码
   - 特别注意安全相关代码 (认证、授权)
   - 运行安全扫描工具

3. **依赖管理:**
   - 定期更新依赖版本
   - 使用 `pip-audit` 检查漏洞

4. **访问控制:**
   - 限制 Git 提交权限
   - CI/CD 使用受保护的分支

## 故障排查

### 问题: API 调用失败

**检查清单:**
- [ ] API Key 是否正确
- [ ] 网络连接是否正常
- [ ] 是否达到 API 限额
- [ ] 提供商服务是否可用

### 问题: 代码解析失败

**可能原因:**
- LLM 未按格式返回代码块
- 提示词模板需要调整

**解决方案:**
- 检查 `step2_code.json` 中的原始响应
- 调整 `claude_code_prompt.txt` 模板

### 问题: 测试失败

**检查:**
- 生成的代码语法是否正确
- 依赖是否完整
- 测试环境是否正确配置

## 下一步开发

### 短期目标

- [ ] 支持更多编程语言
- [ ] 添加 UI 界面
- [ ] 改进错误提示
- [ ] 增加测试覆盖率

### 长期目标

- [ ] 支持微服务架构生成
- [ ] 集成数据库迁移
- [ ] 自动化部署
- [ ] 多人协作支持

---

**维护者:** AI Pipeline Team
**最后更新:** 2024-01
