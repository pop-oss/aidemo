#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 代码流水线演示脚本
用于快速测试流水线功能 (使用模拟 LLM 响应,无需真实 API Key)
"""
import json
import os
import sys
import tempfile

# 设置 UTF-8 编码输出 (Windows 兼容)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from orchestrator.utils import write_files_from_codeblock, validate_json_response


def demo_srs_generation():
    """演示 SRS 生成步骤"""
    print('\n' + '='*60)
    print('演示 1: SRS 生成')
    print('='*60)

    requirement = "创建一个简单的计算器 API,支持加减乘除"

    # 模拟 Codex 响应
    mock_srs_response = {
        "srs": """# 计算器 API - 软件需求规格说明

## 1. 项目概述
创建一个 RESTful API,提供基本的数学运算功能。

## 2. 功能需求
- FR1: 加法运算 POST /api/add
- FR2: 减法运算 POST /api/subtract
- FR3: 乘法运算 POST /api/multiply
- FR4: 除法运算 POST /api/divide

## 3. 非功能需求
- 响应时间 < 100ms
- 输入验证
- 错误处理

## 4. API 规范
每个端点接受 JSON: {"a": number, "b": number}
返回: {"result": number}
""",
        "tasks": [
            {"module": "api", "file": "calculator/api.py", "task": "实现 API 端点"},
            {"module": "logic", "file": "calculator/calc.py", "task": "实现计算逻辑"},
            {"module": "tests", "file": "tests/test_calc.py", "task": "编写单元测试"}
        ]
    }

    print(f'需求: {requirement}')
    print(f'\nSRS 生成结果:')
    print(json.dumps(mock_srs_response, indent=2, ensure_ascii=False))

    return mock_srs_response


def demo_code_generation(srs_data):
    """演示代码生成步骤"""
    print('\n' + '='*60)
    print('演示 2: 代码生成')
    print('='*60)

    # 模拟 Claude 响应
    mock_code_response = """
以下是实现代码:

```python
# path: calculator/api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/add', methods=['POST'])
def add():
    data = request.json
    result = float(data['a']) + float(data['b'])
    return jsonify({'result': result})

@app.route('/api/subtract', methods=['POST'])
def subtract():
    data = request.json
    result = float(data['a']) - float(data['b'])
    return jsonify({'result': result})
```

```python
# path: calculator/calc.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError('Division by zero')
    return a / b
```

```python
# path: tests/test_calc.py
from calculator.calc import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)
```
"""

    print('代码生成完成!')
    print('生成的文件:')

    # 解析代码块
    import re
    pattern = re.compile(r'```(?:[a-zA-Z0-9]*)\n(?:#|//)\s*path:\s*(.+?)\n([\s\S]*?)```')
    code_blocks = []
    for match in pattern.finditer(mock_code_response):
        path = match.group(1).strip()
        content = match.group(2).strip()
        code_blocks.append((path, content))
        print(f'  - {path} ({len(content)} 字符)')

    # 写入临时目录
    tmpdir = tempfile.mkdtemp(prefix='demo_')
    write_files_from_codeblock(code_blocks, tmpdir)
    print(f'\n代码已保存到: {tmpdir}')

    return mock_code_response, code_blocks, tmpdir


def demo_code_review(code_response):
    """演示代码审查步骤"""
    print('\n' + '='*60)
    print('演示 3: 代码审查')
    print('='*60)

    # 模拟 Codex 审查响应
    mock_review_response = {
        "passed": True,
        "results": [
            "✅ 代码结构清晰",
            "✅ 函数命名规范",
            "✅ 包含错误处理",
            "✅ 单元测试覆盖关键功能"
        ],
        "defects": [],
        "tests": {
            "files": [
                {
                    "path": "tests/test_calc.py",
                    "content": "# 测试代码已在上一步生成"
                }
            ],
            "run_command": "pytest tests/",
            "expected_result": "所有测试应该通过"
        }
    }

    print('审查结果:')
    print(json.dumps(mock_review_response, indent=2, ensure_ascii=False))

    if mock_review_response['passed']:
        print('\n✅ 代码审查通过!')
    else:
        print('\n❌ 代码审查未通过')

    return mock_review_response


def demo_complete_flow():
    """完整流程演示"""
    print('\n' + '='*70)
    print('🚀 AI 代码流水线完整演示 (使用模拟数据)')
    print('='*70)

    # 步骤 1: 生成 SRS
    srs_data = demo_srs_generation()

    # 步骤 2: 生成代码
    code_response, code_blocks, output_dir = demo_code_generation(srs_data)

    # 步骤 3: 审查代码
    review_result = demo_code_review(code_response)

    # 总结
    print('\n' + '='*70)
    print('📊 演示总结')
    print('='*70)
    print(f'✅ 生成的任务数: {len(srs_data["tasks"])}')
    print(f'✅ 生成的文件数: {len(code_blocks)}')
    print(f'✅ 审查状态: {"通过" if review_result["passed"] else "未通过"}')
    print(f'📁 输出目录: {output_dir}')
    print('\n提示: 真实使用时,请配置 API Key 并运行:')
    print('  python orchestrator/orchestrator.py --requirement "你的需求"')


def demo_validation_utils():
    """演示工具函数"""
    print('\n' + '='*60)
    print('演示 4: 工具函数验证')
    print('='*60)

    # 测试 JSON 解析
    test_cases = [
        '{"key": "value"}',
        '```json\n{"key": "value"}\n```',
        'Some text {"key": "value"} more text',
    ]

    print('测试 JSON 解析:')
    for i, test in enumerate(test_cases, 1):
        result = validate_json_response(test)
        print(f'  {i}. 输入: {test[:50]}...')
        print(f'     结果: {result}')


def main():
    """主函数"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        demo_complete_flow()
    elif len(sys.argv) > 1 and sys.argv[1] == '--utils':
        demo_validation_utils()
    else:
        print('AI 代码流水线演示脚本')
        print('\n用法:')
        print('  python demo.py --full   # 完整流程演示')
        print('  python demo.py --utils  # 工具函数演示')
        print('\n或者直接运行以查看所有演示:')
        demo_complete_flow()
        demo_validation_utils()


if __name__ == '__main__':
    main()
