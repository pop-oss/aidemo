# 🌐 第三方 API 使用指南

本指南说明如何配置项目以使用第三方 LLM API(国内代理、兼容 OpenAI 格式的服务等)。

---

## 📋 支持的第三方服务

### 已测试兼容的服务

✅ **ChatAnywhere** (国内代理)
- API 端点: `https://api.chatanywhere.com.cn/v1`
- 支持模型: GPT-4, GPT-3.5

✅ **DeepSeek** (国产大模型)
- API 端点: `https://api.deepseek.com/v1`
- 支持模型: `deepseek-chat`, `deepseek-coder`

✅ **SiliconFlow** (硅基流动)
- API 端点: `https://api.siliconflow.cn/v1`
- 支持多种开源模型

✅ **智谱AI (GLM)**
- API 端点: `https://open.bigmodel.cn/api/paas/v4`
- 支持模型: `glm-4`, `glm-4-0520`

✅ **通义千问 (Qwen)**
- API 端点: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- 支持模型: `qwen-max`, `qwen-turbo`

---

## 🚀 快速配置

### 步骤 1: 创建配置文件

```bash
# 复制第三方 API 配置模板
copy .env.thirdparty.example .env
```

### 步骤 2: 编辑配置文件

打开 `.env` 文件并填写以下信息:

```ini
# LLM Provider (保持为 openai)
LLM_PROVIDER=openai

# 你的 API Key
OPENAI_API_KEY=sk-your-api-key-here

# 第三方 API 端点
OPENAI_API_BASE=https://api.your-provider.com/v1

# 支持的模型名称
OPENAI_MODEL=gpt-4-turbo-preview

# 开启调试模式 (推荐)
DEBUG=true
```

### 步骤 3: 运行项目

```bash
# Windows PowerShell
cd d:/vc_demo/aidemo/ai-pipeline
python orchestrator/orchestrator.py --requirement "创建一个待办事项 API"
```

---

## 📖 详细配置示例

### 示例 1: 使用 DeepSeek

```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-你的DeepSeek-API-Key
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-coder
DEBUG=true
```

### 示例 2: 使用智谱AI (GLM-4)

```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=你的智谱AI-API-Key
OPENAI_API_BASE=https://open.bigmodel.cn/api/paas/v4
OPENAI_MODEL=glm-4
DEBUG=true
```

### 示例 3: 使用通义千问

```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-你的通义千问-API-Key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-max
DEBUG=true
```

### 示例 4: 使用 ChatAnywhere (国内代理)

```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-你的ChatAnywhere-Key
OPENAI_API_BASE=https://api.chatanywhere.com.cn/v1
OPENAI_MODEL=gpt-4
DEBUG=true
```

---

## 🔍 验证配置

### 方法 1: 使用演示脚本

```bash
# 无需 API Key 的演示 (验证项目安装)
python demo.py --full
```

### 方法 2: 简单测试

创建测试脚本 `test_api.py`:

```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key'
os.environ['OPENAI_API_BASE'] = 'https://api.your-provider.com/v1'
os.environ['OPENAI_MODEL'] = 'your-model'
os.environ['DEBUG'] = 'true'

from orchestrator.llm_client import LLMClient

client = LLMClient(provider='openai')
response = client.call_codex('你好,请说一句话')
print(f'API 响应: {response}')
```

运行测试:

```bash
python test_api.py
```

---

## 🐛 故障排查

### 问题 1: 连接超时

**错误信息:**
```
ConnectionError: HTTPSConnectionPool
```

**解决方案:**
- 检查网络连接
- 确认 API 端点地址正确
- 如果在国内,可能需要使用代理

### 问题 2: 401 Unauthorized

**错误信息:**
```
OpenAI API 调用失败: 401 Unauthorized
```

**解决方案:**
- 检查 API Key 是否正确
- 确认 API Key 是否已激活
- 检查账户余额是否充足

### 问题 3: 模型不存在

**错误信息:**
```
model_not_found: The model 'xxx' does not exist
```

**解决方案:**
- 确认 `OPENAI_MODEL` 配置的模型名称正确
- 查看服务商文档确认支持的模型列表
- 尝试使用默认模型

### 问题 4: API 端点格式错误

**常见错误:**
- ❌ `https://api.provider.com` (缺少 /v1)
- ✅ `https://api.provider.com/v1` (正确)

**解决方案:**
- 确保 API 端点以 `/v1` 结尾
- 参考服务商官方文档

### 问题 5: 调试信息不显示

**解决方案:**
```ini
# 确保开启调试模式
DEBUG=true
```

运行时会显示:
```
[DEBUG] LLM Provider: openai
[DEBUG] API Base URL: https://api.xxx.com/v1
[DEBUG] Model: gpt-4
[DEBUG] 使用第三方 API: https://api.xxx.com/v1
```

---

## 💡 使用技巧

### 技巧 1: 选择合适的模型

**推荐模型选择:**

| 任务类型 | 推荐模型 | 说明 |
|---------|---------|------|
| 需求分析 | GPT-4, DeepSeek-Chat | 理解能力强 |
| 代码生成 | GPT-4, DeepSeek-Coder | 编码能力强 |
| 代码审查 | GPT-4, GLM-4 | 逻辑分析能力强 |

### 技巧 2: 降低成本

**使用混合策略:**
```ini
# 主模型使用便宜的模型
OPENAI_MODEL=gpt-3.5-turbo

# 关键步骤手动切换为高级模型
# (需要修改代码中的模型参数)
```

### 技巧 3: 提高成功率

```bash
# 增加重试次数
python orchestrator/orchestrator.py \
  --requirement "你的需求" \
  --max-iterations 3
```

### 技巧 4: 调试 API 调用

开启调试模式查看详细信息:

```ini
DEBUG=true
```

输出示例:
```
[DEBUG] LLM Provider: openai
[DEBUG] API Base URL: https://api.deepseek.com/v1
[DEBUG] Model: deepseek-coder
[DEBUG] 使用第三方 API: https://api.deepseek.com/v1
正在调用 Codex 生成 SRS...
API 调用成功! (响应时间: 2.3s)
```

---

## 📊 性能比较

基于简单项目测试 (待办事项 API):

| 服务商 | 模型 | 响应时间 | 代码质量 | 成本 |
|--------|------|---------|---------|------|
| OpenAI | GPT-4 | ~30s | ⭐⭐⭐⭐⭐ | $$$$ |
| DeepSeek | deepseek-coder | ~15s | ⭐⭐⭐⭐ | $ |
| 智谱AI | GLM-4 | ~20s | ⭐⭐⭐⭐ | $$ |
| 通义千问 | qwen-max | ~18s | ⭐⭐⭐⭐ | $$ |

---

## 🔗 获取 API Key

### DeepSeek
1. 访问 [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. 注册账号并充值
3. 创建 API Key

### 智谱AI (GLM)
1. 访问 [https://open.bigmodel.cn/](https://open.bigmodel.cn/)
2. 注册并实名认证
3. 创建 API Key

### 通义千问
1. 访问 [https://dashscope.aliyun.com/](https://dashscope.aliyun.com/)
2. 注册阿里云账号
3. 开通服务并获取 API Key

### SiliconFlow
1. 访问 [https://siliconflow.cn/](https://siliconflow.cn/)
2. 注册账号
3. 创建 API Key

---

## ❓ 常见问题

**Q: 是否必须使用 OpenAI 官方 API?**

A: 不需要!项目支持任何兼容 OpenAI 格式的 API,包括国内的各种代理和国产大模型。

**Q: 如何知道我的第三方服务是否兼容?**

A: 如果服务商声称"兼容 OpenAI API 格式"或提供类似的 `chat.completions.create()` 接口,通常都可以使用。

**Q: 可以同时配置多个 API 吗?**

A: 当前版本不支持。但你可以创建多个 `.env` 文件(如 `.env.deepseek`, `.env.glm`)并在运行时指定。

**Q: 第三方 API 的代码质量如何?**

A: 取决于具体模型。建议先用演示脚本测试,然后根据结果选择最适合的服务。

---

## 🎯 推荐配置

### 适合国内用户

```ini
# DeepSeek - 性价比高,代码能力强
LLM_PROVIDER=openai
OPENAI_API_KEY=your-deepseek-key
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-coder
DEBUG=true
```

### 适合预算充足用户

```ini
# OpenAI GPT-4 (通过国内代理)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_API_BASE=https://api.chatanywhere.com.cn/v1
OPENAI_MODEL=gpt-4
DEBUG=true
```

---

**配置完成后,运行项目:**

```bash
python orchestrator/orchestrator.py --requirement "创建一个用户认证 API"
```

祝使用愉快! 🎉
