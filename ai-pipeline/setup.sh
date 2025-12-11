#!/bin/bash
# AI 代码流水线快速设置脚本

set -e

echo "🚀 AI 代码流水线 - 快速设置"
echo "=============================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要 Python $required_version 或更高版本"
    echo "   当前版本: $python_version"
    exit 1
fi
echo "✅ Python 版本: $python_version"
echo ""

# 创建虚拟环境
echo "创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
echo "✅ 虚拟环境已激活"
echo ""

# 安装依赖
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ 依赖安装完成"
echo ""

# 创建 .env 文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "✅ .env 文件已创建,请编辑并填入你的 API Key"
    echo ""
    echo "⚠️  重要: 请编辑 .env 文件并设置以下变量:"
    echo "   - OPENAI_API_KEY=your-key"
    echo "   - CLAUDE_API_KEY=your-key (可选)"
    echo "   - LLM_PROVIDER=openai"
    echo ""
else
    echo "✅ .env 文件已存在"
    echo ""
fi

# 运行测试
echo "运行测试验证安装..."
if pytest example_app/tests/ -v -q; then
    echo "✅ 测试通过!"
else
    echo "⚠️  部分测试失败,但不影响主流程"
fi
echo ""

echo "=============================="
echo "✅ 设置完成!"
echo ""
echo "下一步:"
echo "  1. 编辑 .env 文件,设置 API Key"
echo "  2. 运行流水线:"
echo "     python orchestrator/orchestrator.py --requirement '你的需求'"
echo ""
echo "示例:"
echo "  python orchestrator/orchestrator.py --requirement '创建一个用户认证 API'"
echo ""
echo "查看帮助:"
echo "  python orchestrator/orchestrator.py --help"
echo ""
