#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 代码流水线启动脚本
自动加载 .env 文件中的环境变量
"""
import os
import sys

# 加载 .env 文件
from dotenv import load_dotenv

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

# 加载环境变量
if os.path.exists(env_file):
    load_dotenv(env_file)
    print(f'✓ 已加载环境配置: {env_file}')
else:
    print(f'⚠️  未找到 .env 文件: {env_file}')
    print('提示: 复制 .env.thirdparty.example 为 .env 并填写配置')
    sys.exit(1)

# 验证必需的环境变量
if not os.getenv('OPENAI_API_KEY'):
    print('❌ 错误: 未设置 OPENAI_API_KEY')
    print('请在 .env 文件中配置 OPENAI_API_KEY')
    sys.exit(1)

# 显示配置信息 (调试模式)
if os.getenv('DEBUG', 'false').lower() == 'true':
    print('\n配置信息:')
    print(f'  Provider: {os.getenv("LLM_PROVIDER", "openai")}')
    print(f'  API Base: {os.getenv("OPENAI_API_BASE", "默认")}')
    print(f'  Model: {os.getenv("OPENAI_MODEL", "默认")}')
    print()

# 导入并运行主程序
sys.path.insert(0, os.path.join(script_dir, 'orchestrator'))
from orchestrator import main
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AI 自动化代码流水线 - 从需求到可运行代码'
    )
    parser.add_argument(
        '--requirement',
        required=True,
        help='用户需求描述'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=2,
        help='最大修复迭代次数 (默认: 2)'
    )

    args = parser.parse_args()
    main(args.requirement, args.max_iterations)
